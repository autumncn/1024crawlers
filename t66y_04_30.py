import urllib.request
import urllib.parse
import os
import json
import time
import re
import base64
import sys
from selenium import webdriver

def url_open(url):
	req = urllib.request.Request(url)	
	req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36')
	response = urllib.request.urlopen(req)
	html = response.read()
	return html

def get_page(url, page_num):
	new_url = url + '&search=&page=' + str(page_num)
	return new_url

def get_page_info(url):
	html = url_open(url).decode('gbk')
	get_time_int = int(time.strftime('%Y%m%d',time.localtime(time.time())))
	
	print(url)
	page_info= [] # page_info 中包含地址，日期，名称，用：隔开

	pattern2 = '<.*?(href=".*?</a>).*?'
	html_str = str(html)
	
	content_href = re.findall(pattern2,html_str,re.I)
	
	set2 = set(content_href)
	for j in set2:
		a_url = str(j)
		if '.html' in a_url:
			bt_url=a_url[0:a_url.index(' target="_blank"')]
			if '<font color=red>' in a_url or '注意事項' in a_url or '版規' in a_url:
				continue
			# bt_url=bt_url.replace('href="','http://t66y.com/').replace('"','')
			bt_url=bt_url.replace('href="','').replace('"','')
			# print(bt_url)
			bt_name=a_url[a_url.index('target="_blank" id="">')+22:a_url.index('</a>')]
			
			page_info_each = bt_url + ':' + bt_name + ':' + str(get_time_int)
			page_info.append(page_info_each)  

	# print(page_info)
	return page_info

def find_imgs(url):
	print('searching IMG files in this url page')
	html = url_open(url).decode('gbk')
	
	img_addrs = []

	pattern1 = "<.*?(ess-data='https://.*?').*?"
	data_str = str(html)
	# print(data_str)
	content_href = re.findall(pattern1,data_str,re.I)
	set1 = set(content_href)
	# file_new = "herf.txt"
	# with open(file_new,'w') as f:
	for i in set1:
		pic_url = str(i)
		if '.jpg' in pic_url:
			pic_url=pic_url.replace("ess-data='","").replace("'","").replace("https","http")
			print(str(pic_url))
			img_addrs.append(pic_url)
	# print(img_addrs)
	return img_addrs

def find_bt_path(url):
	html = url_open(url).decode('gbk')

	bt_addrs = []
	# print(url)
	a = html.find('http://www.rmdown.com/link')
	while a != -1:
		b = html.find('<', a, a + 300)
		# img_hash = domain_url +'/' + html[a+10:b+4]
		if b != -1:
			bt_path = html[a:b]
			bt_addrs.append(bt_path)
		else:
			b = a + 36

		a = html.find('http://www.rmdown.com/link', b)
	return bt_addrs

def save_imgs(folder, img_addrs):
	print('Saving IMG files')
	filename = ''
	for each in img_addrs:
		filename = each.split('/')[-1]	
		# print(filename)
		print(each)
		with open(filename, 'wb') as f:
			img = url_open(each)
			f.write(img)

def save_paths(folder, bt_paths):
	print('Saving BT Path to file')
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
	print('Downloading BT Files')
	for each in bt_paths:
		# print(each)
		try:
			driver.get(each);
			driver.find_element_by_xpath(".//*[@type='submit']").submit()     #采用type
			time.sleep(55)
			# time.sleep(5)
			driver.quit()     #关闭并退出浏览器 	 
		except:
			print('bt download error on ' +  each)
			time.sleep(30)
			# time.sleep(5)
			driver.quit()     #关闭并退出浏览器 	 

# def download_mm(folder='t66y.com', pages=1):
def download_mm(folder, pages, url):
# def download_mm(folder='t66y.com', pages=1):

	if os.path.exists(folder):
		pass
	else:
		os.mkdir(folder)
	os.chdir(folder)

	get_time = time.strftime('%Y.%m.%d',time.localtime(time.time()))
	# print(get_time)
	if os.path.exists(get_time):
		pass
	else:
		os.mkdir(get_time)
	os.chdir(get_time)	

	url_pos1 = url.find('.com/')
	domain_url = url[0:url_pos1+5]
	print(domain_url)

	page_num = pages
	print("Downloading ...")

	for i in range(pages):
		page_url = get_page(url, page_num)
		folder_name = page_url.replace('\\', '').replace('.', '').replace('/', '').replace('_', '')
		if os.path.exists(folder_name):
			pass
		else:
			os.mkdir(folder_name)
		os.chdir(folder_name)	

		page_infos = get_page_info(page_url)
		# print(page_infos)

		for each in page_infos:
			file_url = each.split(':')[0]	
			file_name = each.split(':')[1]	
			file_date = each.split(':')[2]	
			file_name = file_name[0:25].replace('\\', '').replace('.', '').replace('/', '').replace('_', '')

			sub_url = domain_url + 	file_url
			print(str(sub_url))
			img_addrs = find_imgs(sub_url)

			if os.path.exists(file_name):
				pass
			else:
				os.mkdir(file_name)
			os.chdir(file_name)
			# save_paths(sub_folder_name, img_addrs)			
			save_imgs(file_name, img_addrs)	

			bt_paths = find_bt_path(sub_url)
			# print(bt_paths)
			if bt_paths != '[]':
				save_paths(file_name, bt_paths)			

				options = webdriver.ChromeOptions()
				# prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': os.getcwd()}
				prefs = {'download.default_directory': os.getcwd(),'download.prompt_for_download': False,'download.directory_upgrade': True,'safebrowsing.enabled': False,'safebrowsing.disable_download_protection': True}

				options.add_experimental_option('prefs', prefs)

				options.add_argument('--headless')
				options.add_argument('--disable-gpu')
				options.add_argument('--no-sandbox') # 这个配置很重要
				# driver = webdriver.Chrome('/usr/local/bin/chromedriver',options=options)
				driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver',options=options)
				driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
				params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': os.getcwd()}}
				command_result = driver.execute("send_command", params)
				# print("response from browser:")
				for key in command_result:
					# print("result:" + key + ":" + str(command_result[key]))

					save_bt_file(file_name, bt_paths, driver)			

			os.chdir(os.path.dirname(os.getcwd()))

		page_num -= i
		os.chdir(os.path.dirname(os.getcwd()))
	
	print("Retrieve Completed")
	driver.quit()     #关闭并退出浏览器 

	os.chdir(os.path.dirname(os.getcwd()))
	os.chdir(os.path.dirname(os.getcwd()))

if __name__ == '__main__':
	# pages = 1
	download_mm('t66y.com', 1, 'http://t66y.com/thread0806.php?fid=2') # wu ma
	download_mm('t66y.com', 1, 'http://t66y.com/thread0806.php?fid=15') # you ma









