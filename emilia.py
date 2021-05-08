from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor




def main():
    from kivy.lang import Builder
    from kivy.app import App

    class Application(App):

        def start(self):
            self.root.ids.ok.disabled = False
            self.root.ids.save_message.disabled = False
            self.root.ids.start.disabled = True
            self.driver = webdriver.Chrome(executable_path=r"C:\Users\niyas\Desktop\Dev\miscellaneous\WebDrivers\chromedriver.exe") 
            self.driver.get('https://web.whatsapp.com/')
            self.root.ids.progress.text = 'Waiting!!'


        def ok(self):
            self.root.ids.ok.disabled = True
            self.root.ids.save_message.disabled = True
            self.root.ids.progress.text = 'Under Progress!!'

            with ThreadPoolExecutor(max_workers=2) as thread:
                thread.submit(self.process)

        
        def process(self):
            page_source = BeautifulSoup(self.driver.page_source, 'lxml')

            reload_message_element = '_3M4BR'

            chat_body_element = '_1gL0z'

            message_element = 'copyable-text'

            chat_body = self.driver.find_element_by_class_name(chat_body_element)

            while(page_source.find('div', {'class':reload_message_element})):

                for _ in range(10):
                    chat_body.send_keys(Keys.PAGE_UP)
                page_source = BeautifulSoup(self.driver.page_source, 'lxml')

            messages = page_source.findAll('div', {'class':message_element})

            count = len(messages)

            if self.save_flag:
                with open('messages.txt', 'w') as file:
                    for message in messages:
                        file.write(f"{message.get('data-pre-plain-text')} {message.text}\n")

            self.root.ids.progress.text = f'Done!! Total number of messages = {count}!!'

        


        def save(self, instance, value):
            self.save_flag = value
            print(self.save_flag)


        def build(self):
            return Builder.load_file('emilia.kv')

    Application().run()








if __name__ == '__main__':
    main()