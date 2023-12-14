from urllib.error import HTTPError

import math
import urllib.request
import time

from dns.active_measure import LoadMeasurer
from utils.util import Utils


class GeoIPLocator:
    API_URL = "https://api.freegeoip.app/json/"

    # Keys to be used to look up geological information of IPs
    API_KEYS = ["cbfc9480-57a2-11ec-8ad8-833775a8b221", "d5599360-588e-11ec-afec-95107239d823",
                "0917de70-588f-11ec-89a3-3fc3e9907aec", "24884a50-588f-11ec-b303-3fbfa2ec5ff0"]

    API_KEY_INDEX = 0

    DNS_IP_FILE_LOCATION = "./dns-hosts.txt"

    # Constructor for the class
    def __init__(self, https_replica_file_location):
        # Used to store all replica IPS
        self.replica_IPs = []
        # Used to store locations of replica IPs
        self.IP_locations = []
        # Used to cache the location data of the client ip
        self.client_to_replica_distances = {}
        # Location of dns server
        self.dns_location = None
        # Used to store distance from dns to replica IPs.
        self.distance_to_replicas = []

        # Find DNS location from IP address
        try:
            dns_ip = Utils.get_file_contents(self.DNS_IP_FILE_LOCATION).strip().decode()
            dns_ip_details = self.get_IP_details(dns_ip)
            self.dns_location = (dns_ip_details['latitude'], dns_ip_details['longitude'])
        except Exception as ex:
            print (ex)

        # Read all the replica IP addresses from the file on the server.
        for ip in Utils.get_file_contents(https_replica_file_location).decode().split("\n"):
            ip = ip.strip()
            if ip:
                self.replica_IPs.append(ip)

        # Cache the location of replica IP addresses. We will use them later to find the closest replica to the client.
        # In case of rate limit or other errors switch to round robin method to redirect clients.
        try:
            for ip in self.replica_IPs:
                ip_details = self.get_IP_details(ip)
                self.IP_locations.append((ip_details['latitude'], ip_details['longitude']))
        except:
            self.IP_locations = None

        # Find distance from DNS to all replicas which is used later where scamper output doesn't have information
        # about a particular replica.
        if self.dns_location is not None:
            for replica_location in self.IP_locations:
                dns_to_rep_distance = Utils.get_distance_between_coordinates(replica_location, self.dns_location)
                self.distance_to_replicas.append(dns_to_rep_distance)

        # Object used to handle active measurements.
        self.load_measurer = LoadMeasurer(self, 60)


    # Get geological location of the IP address passed.
    def get_IP_details(self, ip_address):

        request = urllib.request.Request(self.API_URL + ip_address + "?apikey=" + self.API_KEYS[GeoIPLocator.API_KEY_INDEX])
        output = None
        try:
            output = urllib.request.urlopen(request)
        except HTTPError as geo_ip_ex:
            print(geo_ip_ex)
            if geo_ip_ex.code >= 400:
                GeoIPLocator.API_KEY_INDEX = (GeoIPLocator.API_KEY_INDEX + 1) % len(self.API_KEYS)


        # In case the API fails to get the location data then throw an exception.
        if output is None or output.status != 200:
            raise Exception("Failed to get location details for " + ip_address)
        res = {}
        # Read latitude and longitude
        for line in output.read().decode().split(","):
            if "latitude" in line:
                res["latitude"] = float(line.split(":")[1])
                pass
            if "longitude" in line:
                res["longitude"] = float(line.split(":")[1])
                pass
        output.close()

        return res

    def remove_bad_replicas_helper(self, distance_index_pairs):
        # Get ratings based on the load on the replica servers.
        # Rating 0 means the server is up and under normal load
        # Rating -1 means the server is under high load
        # Rating -2 means the server is under extremely high load.
        replica_ip_ratings_pairs = self.load_measurer.get_replica_ratings()

        # Prioritise the closest replica server which is under normal load.
        for _, index in distance_index_pairs:

            replica_at_index = self.replica_IPs[index]

            # If rating is zero use the closest
            if replica_at_index in replica_ip_ratings_pairs and replica_ip_ratings_pairs[replica_at_index] == 0:
                return replica_at_index
        # If no replica server is under normal load then find the server under high load.
        for _, index in distance_index_pairs:
            replica_at_index = self.replica_IPs[index]
            # If rating is one use the closest
            if replica_at_index in replica_ip_ratings_pairs and replica_ip_ratings_pairs[replica_at_index] == -1:
                return replica_at_index
        # If no servers under normal and high load are found return the originally closest server
        return self.replica_IPs[distance_index_pairs[0][1]]

    def remove_bad_replicas_from_closest(self, distance_index_pairs):
        return self.remove_bad_replicas_helper(distance_index_pairs)

    # Get the closest replica to the IP address passed in the parameter.
    def get_closest_ip(self, source_ip):
        # Check if client has already been seen.
        if source_ip in self.client_to_replica_distances:
            return self.remove_bad_replicas_from_closest(self.client_to_replica_distances[source_ip][1])
        # If this is the first time seeing the client, calculate the distances between
        # the client and every replica.
        distances = []
        # Get location of the source IP address.
        source_ip_details = self.get_IP_details(source_ip)
        source_ip_location = (source_ip_details['latitude'], source_ip_details['longitude'])
        for ii, dest_ip_loc in enumerate(self.IP_locations):
            # Calculate the distance between source & destination.
            cur_dis = Utils.get_distance_between_coordinates(source_ip_location, dest_ip_loc)
            distances.append((cur_dis, ii))
        # Sort distances to identify the closest server.
        distances = sorted(distances)
        self.client_to_replica_distances[source_ip] = (time.time(), distances)
        # Limit caching to store data of only 1000 IPs
        if len(self.client_to_replica_distances.keys()) > 1000:
            del self.client_to_replica_distances[self.client_to_replica_distances.keys()[0]]

        # Return the closest replica's IP address which is performing better than others (active measurements).
        return self.remove_bad_replicas_from_closest(self.client_to_replica_distances[source_ip][1])
