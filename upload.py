    def __set_scheduler(self):
        # Set upload time
        action = ActionChains(self.browser.driver)
        schedule_radio_button = self.browser.driver.find_element_by_id("schedule-radio-button")

        action.move_to_element(schedule_radio_button)
        action.click(schedule_radio_button).perform()
        self.logger.debug('Set delevery to {}'.format("schedule"))
        time.sleep(.33)

        #Set close action
        action_close = ActionChains(self.browser.driver)
        action_close.send_keys(Keys.ESCAPE)

        #date picker
        action_datepicker = ActionChains(self.browser.driver)
        datepicker_trigger = self.browser.driver.find_element_by_id("datepicker-trigger")

        action_datepicker.move_to_element(datepicker_trigger)
        action_datepicker.click(datepicker_trigger).perform()
        time.sleep(.33)

        date_string = self.metadata["release_date"].strftime("%d.%m.%Y")
        date_input = self.browser.driver.find_element_by_xpath('//ytcp-date-picker/tp-yt-paper-dialog//iron-input/input')

        self.__write_in_field(date_input, date_string, True)
        self.logger.debug('Set schedule date to {}'.format(date_string))

        action_close.perform()
        time.sleep(.33)


        #time picker
        action_timepicker = ActionChains(self.browser.driver)
        time_of_day_trigger = self.browser.driver.find_element_by_id("time-of-day-trigger")
        
        action_timepicker.move_to_element(time_of_day_trigger)
        action_timepicker.click(time_of_day_trigger).perform()
        time.sleep(.33)

        time_dto = (self.metadata["release_date"] - timedelta( 
                            minutes = self.metadata["release_date"].minute % 15,
                            seconds = self.metadata["release_date"].second,
                            microseconds = self.metadata["release_date"].microsecond))
        time_string = time_dto.strftime("%H:%M")
        
        time_container = self.browser.driver.find_element_by_xpath('//ytcp-time-of-day-picker//*[@id="dialog"]')
        time_item = self.browser.driver.find_element_by_xpath('//ytcp-time-of-day-picker//tp-yt-paper-item[text() = "{}"]'.format(time_string))
        
        self.logger.debug('Set schedule date to {}'.format(time_string))
        self.browser.driver.execute_script("arguments[0].scrollTop = arguments[1].offsetTop; ", time_container, time_item)

        time_item.click()

        action_close.perform()
        time.sleep(.33)

