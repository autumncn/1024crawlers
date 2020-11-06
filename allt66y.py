import urllib.request
import urllib.parse
import os
import json
import time
import re
import base64
import sys
from selenium import webdriver
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import random


USER_AGENTS = [
#    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 12_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/73.0.3683.68 Mobile/15E148 Safari/605.1",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
#    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.2 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
	"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36"
]

XFF = [
    "58.59.8.81",
    "112.85.42.45",
	"61.130.181.253",
	"218.23.69.10",
	"222.79.191.34",
	"218.5.177.10",
	"182.101.185.10",
	"58.59.8.82",
	"120.224.227.106",
	"222.89.114.114",
	"115.50.162.108",
	"61.184.189.46",
	"223.151.49.29",
	"113.117.108.128",
	"47.106.168.59",
	"222.217.30.45",
	"223.198.230.68",
	"27.11.137.113",
	"101.207.225.79",
	"221.10.205.22",
	"182.241.130.122"
	"113.138.130.195",
	"223.220.250.158",
	"14.134.188.247",
	"168.63.151.20",
	"103.99.51.20",
	"47.241.72.7",
	"47.88.61.197",
	"35.201.211.246"
]

def url_open(url):
	req = urllib.request.Request(url)	
	# req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36')
	req.add_header('User-Agent', random.choice(USER_AGENTS))
	req.add_header('X-Forwarded-For', random.choice(XFF))	
	response = urllib.request.urlopen(req)
	html = response.read()
	return html

def find_imgs(url):
	html = url_open(url).decode('gbk')
	# url_pos1 = url.find('.com/')
	# domain_url = url[0:url_pos1+5]

	img_addrs = []

	# http://img599.net/images/2018/09/15/j2018-0917-24.th.jpg
	
	pattern1 = r"ess-data='(.*?)'>&nbsp;"
	get_link_content = re.findall(pattern1,html,re.I)
	# print(get_link_content)
	set1 = set(get_link_content)
	for i in set1:
		if "<" in str(i):
			continue
		if ".j" in str(i):
			img_addrs.append(str(i))
	# print(img_addrs)
	return img_addrs

def find_bt_path(url):
	html = url_open(url).decode('gbk')

	bt_addrs = []
	print(url)

	pattern1 = r"http://www.rmdown.com/link.php(.*?)</a>"
	get_link_content = re.findall(pattern1,html,re.I)
	# print(get_link_content)
	set1 = set(get_link_content)
	for i in set1:
		if "<" in str(i):
			continue
		if "hash" in str(i):
			bt_addrs.append("http://www.rmdown.com/link.php" + str(i))
	# print(bt_addrs)	
	return bt_addrs

def save_imgs(folder, img_addrs):
	filename = ''
	for each in img_addrs:
		filename = each.split('/')[-1]	
		# print(filename)
		print(each)
		with open(filename, 'wb') as f:
			img = url_open(each)
			f.write(img)

def save_paths(folder, bt_paths):
	msg = ''
	filename = ''
	for each in bt_paths:
		filename = each.split('/')[-1]	
		print(each)
		msg = msg + each + '\n'
	full_path = folder + filename + '.txt' 
	file = open(full_path,'w')             
	file.write(msg) 
	file.close() 
		# print('File saved')

def save_bt_file(folder, bt_paths, driver):
	for each in bt_paths:
		print(each)
		try:
			driver.get(each);
			driver.find_element_by_xpath(".//*[@type='submit']").submit()     #采用type
			time.sleep(3)
			driver.quit()     #关闭并退出浏览器 	 
		except:
			print('bt download error on ' +  each)
			time.sleep(3)
			driver.quit()     #关闭并退出浏览器 	 

def create_folder(folder='t66y.com'):
	if os.path.exists(folder):
		pass
	else:
		os.mkdir(folder)
	os.chdir(folder)

def get_post_pages(pages=1, type=15):
	base_url = 'http://t66y.com/thread0806.php?fid=' + str(type)   #you
	create_folder(str(type))

	link_datas = []
	for i in range(0,pages):
		# http://t66y.com/thread0806.php?fid=15&search=&page=1
		url = base_url + "&search=&page=" + str(i)
		html = url_open(url).decode('gbk')

		pattern1 = r'<h3><a href="htm_data(.*?)</a></h3>'
		get_link_content = re.findall(pattern1,html,re.I)
		# print(get_link_content)
		set1 = set(get_link_content)
		for i in set1:
			link_data = []
			get_link_pos = i.find('" target="_blank" id="">') 
			get_link = "http://t66y.com/htm_data" + i[:get_link_pos]
			link_data.append(get_link)
			get_name = str(i[get_link_pos+24:]).replace(" ","").replace("[","").replace("]","").replace("/","").replace("\\","").replace(";","").replace(",","").replace("*","").replace("~","").replace("&nbsp","")   
			link_data.append(get_name[:40])
			link_data.append(get_name)
			if "事項" in get_name or "版規" in get_name or ">" in get_name:
				continue
			link_datas.append(link_data)
	# print(link_datas)
	return link_datas
#	url = 'http://t66y.com/thread0806.php?fid=2'	#wu

def get_handle_page(link_datas):
	# test_num = 0
	for link_data in link_datas:
		# test_num = test_num +1
		# if test_num > 4:
		# 	break

		try:
			sub_url = link_data[0]
			file_name = link_data[1]
			create_folder(file_name)

			print(sub_url)
			print(file_name)
			img_addrs = find_imgs(sub_url)
			save_imgs(file_name, img_addrs)	

			bt_addrs = find_bt_path(sub_url)
			save_paths(file_name, bt_addrs)

			if bt_addrs != '[]':
				options = webdriver.ChromeOptions()
				# prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': os.getcwd()}
				prefs = {'download.default_directory': os.getcwd(),'download.prompt_for_download': False,'download.directory_upgrade': True,'safebrowsing.enabled': False,'safebrowsing.disable_download_protection': True}

				options.add_experimental_option('prefs', prefs)
				# driver = webdriver.Chrome(chrome_options=options)
				# driver.maximize_window()

				options.add_argument('--headless')
				options.add_argument('--disable-gpu')
				options.add_argument('--no-sandbox') # 这个配置很重要
				# driver = webdriver.Chrome('/usr/local/bin/chromedriver',chrome_options=options)
				driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver',chrome_options=options)
				driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
				params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': os.getcwd()}}
				command_result = driver.execute("send_command", params)
				print("response from browser:")
				for key in command_result:
					print("result:" + key + ":" + str(command_result[key]))

				save_bt_file(file_name, bt_addrs, driver)	
			
			os.chdir(os.path.dirname(os.getcwd()))
		except Exception as e:
			print(e)	
	
	os.chdir(os.path.dirname(os.getcwd()))

	print("Retrieve Completed")
	driver.quit()    

if __name__ == '__main__':
	get_time = time.strftime('%Y.%m.%d',time.localtime(time.time()))

	create_folder('t66y.com')
	create_folder(get_time)

	# download_mm()
	print("Downloading ...")

	get_page_links = get_post_pages(1,2)
	get_handle_page(get_page_links)

	get_page_links = get_post_pages(1,15)
	get_handle_page(get_page_links)









