#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#https://github.com/michael-stajer/stripe-subscription-scaffold-python/blob/master/main.py
import webapp2
import jinja2
import os
import stripe
import logging
import json




JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    autoescape=True,
    extensions=['jinja2.ext.autoescape'])


class SubscribeHandler(webapp2.RequestHandler):
    def post(self):
        form_stripeToken = self.request.get('stripeToken')
        form_keys = self.request.params
        # 1. valid token or free plan
        try:

            if plan != 'free' and len(form_stripeToken) == 0:
                # invalidtokenerror
                pass

            else:
                pass

            # 2. upsert stripe_customer_id with stripeToken
            # - if we are downgrading to free plan, no stripeToken
            # - can submit customer even if already exists, won't duplicate
            # - can NOT submit empty source, must omit if no source
            # - if source, then response: customer.sources dict card info
            # - customer.sources[0].brand
            # - customer.sources[0].last4

            # 3. subscribe stripe_customer_id to plan

            # 4. display confirmation

        except:
            # logging(e)
            pass

        customer = stripe.Customer.create(
            email="jenny.rosen@example.com",
            source=form_stripeToken,
        )

        subscribe = stripe.Subscription.create(
            customer=customer.id,
            items=[
                {
                    "plan": "basic-monthly",
                },
            ],
        )

        trial_end = subscribe.trial_end
        subscription_start = subscribe.start
        subscription_status = subscribe.status
        subscription_period_end = subscribe.current_period_end
        subscription_id = subscribe.id

        import datetime 
        datetime.datetime.utcfromtimestamp(int("1284101485")).strftime('%Y-%m-%d %H:%M:%S')

        variables = {
            'st': form_stripeToken,
            'keys': form_keys,
            'stripe_customer': customer,
            'stripe_customer_id': customer.id,
            'stripe_subscribe': subscribe
        }

        template = 'templates/subscribe.html'
        template = JINJA_ENVIRONMENT.get_template(template)
        self.response.write(template.render(variables))


class WebhookHander(webapp2.RequestHandler):

    def get(self):
        # Retrieve the request's body and parse it as JSON
        try:
            event_json = json.loads(self.request.body)
            # Do something with event_json

            if event_json.data.object.object == 'subscription':
                stripe_customer_id = event_json.data.object.customer
                status = event_json.data.object.status
                end_at = event_json.data.object.current_period_end

                # customer.subscription.created
                # customer.subscription.deleted

                logging.info(stripe_customer_id, status, end_at)

                # update profilemodel

            logging.info('webhook success' & event_json)
            self.response.status_int = 200
            self.response.write('1')

        except:
            logging.info('webhook error', self.request.body)
            self.response.status_int = 501


class MainHandler(webapp2.RequestHandler):
    def get(self):
        variables = {}
        template = "templates/main.html"
        template = JINJA_ENVIRONMENT.get_template(template)
        self.response.write(template.render(variables))


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/subscribe', SubscribeHandler),
    ('/webhook', WebhookHander)
], debug=True)