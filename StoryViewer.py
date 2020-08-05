import requests,time
import urllib
import json

class account:

	def __init__(self):
		self.s = requests.Session()
		var = self.s.get('https://i.instagram.com/').cookies['csrftoken']# get csrftoken
		self.s.headers ={
			'user-agent':'Mozilla/5.0 (Linux; Android 4.1.2; HTC One Build/JZO54K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.126 Mobile Safari/537.36',
			'X-CSRFToken':var# L:
		}


	def loginAc(self):

		url = 'https://i.instagram.com/accounts/login/ajax/'

		try:
			user = input('Username : ');password  = input('Password : ')
		except:
			print('Error :{')


		data = {
			'username':user,
			'enc_password':f'#PWD_INSTAGRAM_BROWSER:0:{time.time()}:{password}'
		};


		setData = self.s.post(url,data)
	
		
		if setData.json()['authenticated'] == True:
			print('Login Done !')
			csrf = setData.cookies['csrftoken']
			self.s.headers.update({'X-CSRFToken':csrf})
			self.s.cookies.update({'csrftoken':csrf})
			self.ViewStory()
		else:
			print('Error in Login ')




	def ViewStory(self):

		urlGet = 'https://www.instagram.com/graphql/query/?'+urllib.parse.urlencode({

		'query_hash':'7223fb3539e10cad7900c019401669e7',
		"only_stories":'true',
		"stories_prefetch":'false',
		"stories_video_dash_manifest":'false'})
		
		getData = self.s.get(urlGet)
		if getData.status_code == 200:
			print('wAiting !!')
			data_users = getData.json()['data']['user']['feed_reels_tray']['edge_reels_tray_to_reel']['edges']
			id_list = []
			for i in data_users:
				id_list.append(i['node']['id'])
		
			urlGetStory = 'https://www.instagram.com/graphql/query/?query_hash=90709b530ea0969f002c86a89b4f2b8d&variables=%s'%json.dumps(
			{
				"reel_ids":id_list,
				"tag_names":[],
				"location_ids":[],
				"highlight_reel_ids":[],
				"precomposed_overlay":'false',
				"show_story_viewer_list":'true',
				"story_viewer_fetch_count":50,
				"story_viewer_cursor":"",
				"stories_video_dash_manifest":'false'
			}
			)
		
		

			get_stories = self.s.get(urlGetStory).json()['data']['reels_media']
			
			for x in get_stories:
				
				
				user_id = x['id']
				
				stories  = x['items']
				for story in stories:
					
					id_story = story['id']
					seen = story['taken_at_timestamp']
					data = {
							"reelMediaId":id_story,
							"reelMediaOwnerId":user_id,
							"reelId":user_id,
							"reelMediaTakenAt":seen,
							"viewSeenAt":seen
							}
				
					see_story = self.s.post('https://www.instagram.com/stories/reel/seen',data)
					print(see_story.json())
					time.sleep(5)
		else:
			print(getData.status_code)
	def cookies(self):
		sess = ''
		try:
			sess = input('session id : ')

		except:
			print('Enter session id !??')
		
		self.s.cookies.update({'sessionid':sess})
		check = self.s.get('https://www.instagram.com/explore/').status_code

		if check ==200:
			self.ViewStory()
		else: 
			print('Login failed')
		

a = account()
choice = 0
try:
	choice = int(input('login with (user,pass) or Cookies (1,2) : '))
except:
	print('choice 1 or 2 please !!')



if choice ==1:
	a.loginAc()
elif choice ==2:
	a.cookies()
else:
	print('please choice 1 or 2 not : '+str(choice))