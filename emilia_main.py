from concurrent.futures import ThreadPoolExecutor
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys



def main():
    from kivy.app import App
    from kivy.lang import Builder

    class Application(App):

        def start(self):
            self.root.ids.ok.disabled = False
            self.root.ids.save_message.disabled = False
            self.root.ids.start.disabled = True
            self.driver = webdriver.Chrome(executable_path="C:\\Users\\niyas\\Desktop\\Dev\\miscellaneous\\WebDrivers\\chromedriver.exe") 
            self.driver.get('https://web.whatsapp.com/')
            self.root.ids.progress.text = 'Waiting!!'


        def ok(self):
            self.root.ids.ok.disabled = True
            self.root.ids.save_message.disabled = True
            self.root.ids.progress.text = 'Under Progress!!'
            time.sleep(3)
            with ThreadPoolExecutor(max_workers=2) as thread:
                thread.submit(self.process)

        
        def process(self):
            
            page_source = BeautifulSoup(self.driver.page_source, 'lxml')

            reload_message_element = '_3M4BR'

            chat_body_element = '_1gL0z'

            chat_body = self.driver.find_element_by_class_name(chat_body_element)

            while(page_source.find('div', {'class':reload_message_element})):
                for _ in range(10):
                    chat_body.send_keys(Keys.PAGE_UP)
                page_source = BeautifulSoup(self.driver.page_source, 'lxml')

            chat_element = '_11liR'

            message_element = '-1'

            text_element = 'copyable-text'

            chat_screen = page_source.find('div', {'class':chat_element})

            messages = chat_screen.findAll('div', {'tabindex':message_element})

            count = len(messages)

            if self.save_flag:
                with open('messages.txt', 'w') as file:
                    for message in messages:
                        if message.find('div', {'class':'copyable-text'}):
                            ele = message.find('div', {'class':'copyable-text'})
                            file.write(f"{ele.get('data-pre-plain-text')} {message.text[:-5]}\n")

                        else:
                            try:
                                ele = message.find('div', {'class':'_3XpKm _20zqk'})
                                sender = ele.find('span').get('aria-label')
                                if sender:
                                    file.write(f"{sender} Image/audio/document/gif\n")

                                else:
                                    file.write(f"You: Image/audio/document/gif\n")

                            except:
                                try:
                                    if message.find('div', class_ = '').find('span').get('aria-label'):
                                        sender = message.find('div', class_ = '').find('span').get('aria-label')
                                        file.write(f"{sender} sticker\n")
                                    else:
                                        file.write(f"You: sticker\n")
                                except:
                                    pass



            self.root.ids.progress.text = f'Done!! Total number of messages = {count}!!'

            self.driver.quit()

        


        def save(self, instance, value):
            self.save_flag = value
            print(self.save_flag)


        def build(self):
            return Builder.load_file('emilia.kv')

    Application().run()








if __name__ == '__main__':
    main()
