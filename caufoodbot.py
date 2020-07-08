import telegram
from telegram.ext import *
import requests
import threading
from bs4 import BeautifulSoup

global token
token = ''
bot = telegram.Bot(token = token)

def food_info_caching():
	print("학식정보 캐싱중입니다.")
	url = ["MjMyNjY2NzA0","LTIzODA3NTM2","LTIzODAwOTc1","MjIzMDk0MDAx","LTIzODA5NzE5","LTIzODExOTAw"]

	all_info = ""
	for i in url:
		res = requests.get(f"https://bds.bablabs.com/restaurants/{i}?campus_id=biV2tiK41v", headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'})

		soup = BeautifulSoup(res.text,'lxml')
		rest_name = soup.find('h4',class_='card-title').text
		info = ""
		
		if soup.find('div',class_='date-title') != None: # 식단이 없는 경우 date-title이 None으로 표시됨.
			date = soup.find('div',class_='date-title').text
			item = soup.find('div',class_='date-wrapper')
			info += "식당 이름 : " + rest_name + "\n" + date + "\n"
			for food_list in item.findAll('div',class_='card card-menu'):
				info += str(food_list.find('div',class_='card-title').text + "\n")
				info += str(food_list.find('div',class_='card-text').text + "\n")
		else:
			info += "식당 이름 : " + rest_name + "\n등록된 식단이 없습니다.\n"
			
		all_info += info + "\n"
		with open(f'./{rest_name}.txt','w') as fw:
			fw.write(info)
		print(rest_name + " 캐싱 완료.")

	with open('./모든식당.txt','w') as fw:
		fw.write(all_info.strip())
	print("학식정보를 모두 캐싱하였습니다.")

def startTimer():
    food_info_caching()
    timer = threading.Timer(3600, startTimer)
    timer.start()

def checkAndReply():
	try:
		updates = bot.getUpdates()[-1]
		latest_msg = str(updates.message.date)
		username = updates.message.from_user.username

		try:
			with open("old_msg.txt",'r') as fr:
				old_msg = fr.readline()
		except:
			print("creating new files...")
			with open("old_msg.txt",'w') as fw:
				fw.write(latest_msg)

		if(old_msg != latest_msg):
			cmd = updates.message.text
			chat_id = str(updates.message.chat.id)

			fw = open("old_msg.txt",'w')
			fw.write(str(updates.message.date))
			fw.close()

			food_info = ""
			print(username + " 이가")
			if (cmd == "/학식"):
				print("/학식 명령어 사용")
				bot.sendMessage(chat_id = chat_id, text='사용법 : /학식 {번호}\n 0.참슬기식당(310관 B4층)\n 1.기숙사식당(블루미르 308관)\n 2.학생식당(303관 B1층)\n 3.기숙사식당(블루미르 309관)\n 4.교직원식당(303관 B1층)\n 5.University Club(102관 11층)\n 6.모든 식당 보기 \n 7.학식 정보 새로고침 \n * 학식 정보는 자동으로 새로고침 되나 만약 정보가 틀리다면 실행해주세요.')
			elif (cmd == "/학식 0"):
				print("/학식 0 명령어 사용")
				fr = open("참슬기식당(310관 B4층).txt",'r')
				food_read = fr.readlines()
				for i in food_read:
					food_info += i
				fr.close()
				bot.sendMessage(chat_id = chat_id, text=food_info)

			elif (cmd == "/학식 1"):
				print("/학식 1 명령어 사용")
				fr = open("기숙사식당(블루미르 308관).txt",'r')
				food_read = fr.readlines()
				for i in food_read:
					food_info += i
				fr.close()
				bot.sendMessage(chat_id = chat_id, text=food_info)

			elif (cmd == "/학식 2"):
				print("/학식 2 명령어 사용")
				fr = open("학생식당(303관B1층).txt",'r')
				food_read = fr.readlines()
				for i in food_read:
					food_info += i
				fr.close()
				bot.sendMessage(chat_id = chat_id, text=food_info)

			elif (cmd == "/학식 3"):
				print("/학식 3 명령어 사용")
				fr = open("기숙사식당(블루미르 309관).txt",'r')
				food_read = fr.readlines()
				for i in food_read:
					food_info += i
				fr.close()
				bot.sendMessage(chat_id = chat_id, text=food_info)

			elif (cmd == "/학식 4"):
				print("/학식 4 명령어 사용")
				fr = open("교직원식당(303관 B1층).txt",'r')
				food_read = fr.readlines()
				for i in food_read:
					food_info += i
				fr.close()
				bot.sendMessage(chat_id = chat_id, text=food_info)

			elif (cmd == "/학식 5"):
				print("/학식 5 명령어 사용")
				fr = open("University Club(102관 11층).txt",'r')
				food_read = fr.readlines()
				for i in food_read:
					food_info += i
				fr.close()
				bot.sendMessage(chat_id = chat_id, text=food_info)

			elif (cmd == "/학식 6"):
				print("/학식 6 명령어 사용")
				fr = open("모든식당.txt",'r')
				food_read = fr.readlines()
				for i in food_read:
					food_info += i
				fr.close()
				bot.sendMessage(chat_id = chat_id, text=food_info)

			elif (cmd == "/학식 7"):
				print("/학식 7 명령어 사용")
				bot.sendMessage(chat_id = chat_id, text="학식 정보를 새로 받아오고 있습니다..")
				food_info_caching()
				bot.sendMessage(chat_id = chat_id, text="학식 정보를 성공적으로 새로고침 하였습니다.")

			else:
				print("알수없는 " + cmd + " 명령어 사용")
				bot.sendMessage(chat_id = chat_id, text='알수없는 명령어 입니다.\n사용법은 /학식 을 참고하세요.')

		#clear update
		requests.get('https://api.telegram.org/bot'+token+'/getUpdates?offset='+str(updates.update_id))

	except Exception as e:
		print(str(e) +" 예외 발생!")

if __name__ == '__main__':
	startTimer()
	while True:
		checkAndReply()