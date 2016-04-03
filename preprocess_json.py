from collections import defaultdict
import json
from datetime import datetime as dt
import operator
biz = "quebec_biz.json"
review_file = "montreal_reviews.json"
user_file = "montreal_users.json"
# bizlist = []
# with open(biz) as infile: 
# 	for line in infile:
# 		json_decode = json.loads(line)
# 		# bizlist.append(json.loads(line))
# 		print type(json_decode)
		# print line



def get_biz_dict(file):
	biz_dict = defaultdict(list)
	with open(biz) as infile: 
		for line in infile:
			json_decode = json.loads(line)
			# bizlist.append(json.loads(line))
			# print type(json_decode)
			business_id = json_decode["business_id"]
			longitude = json_decode["longitude"]
			latitude = json_decode["latitude"]
			review_count = json_decode["review_count"] 
			# print line
			biz_dict[business_id]=[longitude,latitude,review_count]
	return biz_dict
def get_review_dict(file):
	review_dict = defaultdict(lambda:defaultdict(list))
	review_dict_user_list = defaultdict(list)
	with open(file) as infile: 
		for line in infile:
			json_decode = json.loads(line)

			business_id = json_decode["business_id"]
			user_id = json_decode['user_id']
			review_star = json_decode["stars"]
			date = json_decode["date"]
			date = dt.strptime(date,"%Y-%m-%d")
			review_dict[business_id][user_id].append((review_star,date))
			review_dict_user_list[business_id].append(user_id)
		# break
	return review_dict,review_dict_user_list
def get_friend_dict(file):
	friend_dict = defaultdict(list)
	with open(file) as infile: 
		for line in infile:
			json_decode = json.loads(line)
			friends = json_decode["friends"]
			number_fan = json_decode["fans"]
			user_id = json_decode['user_id']
			friend_dict[user_id] = friends
	return friend_dict
def get_fandict(file):
	fan_dict = defaultdict(list)
	with open(file) as infile: 
		for line in infile:
			json_decode = json.loads(line)
			# friends = json_decode["friends"]
			number_fan = json_decode["fans"]
			user_id = json_decode['user_id']
			fan_dict[user_id] = number_fan
	return fan_dict
def get_incluenc_1():
	biz_dict = get_biz_dict(biz)
	review_dict, review_dict_user_list = get_review_dict(review_file)
	friend_dict = get_friend_dict(user_file)
	influence =defaultdict(lambda:defaultdict(int))
	for business_id, v in review_dict.iteritems():
		# user_id_list = review_dict[business_id][0]
		# print business_id,len(v)
		# break
		user_business = review_dict_user_list[business_id]
		for user_id, vv in v.iteritems():
			for review in vv:
		# user_id = review_dict[business_id]
				date_user = review[1]
				star = review[0]
				friends_of_user = friend_dict[user_id]
				inter_section_user = set(friends_of_user).intersection(set(user_business))
				# date_user = dt.strptime(date_user,"%Y-%m-%d")
				if len(inter_section_user) !=0:
					for friend in inter_section_user:
					    review_friend_list = review_dict[business_id][friend]
					    for review_friend in review_friend_list:
					    	date_friend = review_friend[1]
					    	# date_friend = dt.strptime(review_friend[1] ,"%Y-%m-%d")
					    if date_user < date_friend:
					    	influence[business_id][user_id] +=1
	return influence
	# print influence
	# with open('inclunce1.json','w') as outfile:
	# 	json.dump(influence, outfile)
def get_incluenc_2():
	# divided incluence1 by #friends of the user
	biz_dict = get_biz_dict(biz)
	review_dict, review_dict_user_list = get_review_dict(review_file)
	friend_dict = get_friend_dict(user_file)
	influence =defaultdict(lambda:defaultdict(int))
	for business_id, v in review_dict.iteritems():
		# user_id_list = review_dict[business_id][0]
		# print business_id,len(v)
		# break
		# number_review_buzi = biz_dict[business_id][]
		user_business = review_dict_user_list[business_id]
		for user_id, vv in v.iteritems():
			for review in vv:
		# user_id = review_dict[business_id]
				date_user = review[1]
				star = review[0]
				friends_of_user = friend_dict[user_id]
				number_friend_user = len(friends_of_user)
				inter_section_user = set(friends_of_user).intersection(set(user_business))
				# date_user = dt.strptime(date_user,"%Y-%m-%d")
				if len(inter_section_user) !=0:
					for friend in inter_section_user:
					    review_friend_list = review_dict[business_id][friend]
					    for review_friend in review_friend_list:
					    	date_friend = review_friend[1]
					    	# date_friend = dt.strptime(review_friend[1] ,"%Y-%m-%d")
					    if date_user < date_friend:
					    	influence[business_id][user_id] +=1.0/number_friend_user
	return influence
	# print influence
	# with open('inclunce2.json','w') as outfile:
	# 	json.dump(influence, outfile)

def get_incluenc_3():
	# divided incluence1 by #numbers of reviews for that business
	biz_dict = get_biz_dict(biz)
	review_dict, review_dict_user_list = get_review_dict(review_file)
	friend_dict = get_friend_dict(user_file)
	influence =defaultdict(lambda:defaultdict(int))
	for business_id, v in review_dict.iteritems():
		# user_id_list = review_dict[business_id][0]
		# print business_id,len(v)
		# break
		number_review_bz = biz_dict[business_id][2]
		user_business = review_dict_user_list[business_id]
		for user_id, vv in v.iteritems():
			for review in vv:
		# user_id = review_dict[business_id]
				date_user = review[1]
				star = review[0]
				friends_of_user = friend_dict[user_id]
				# number_friend_user = len(friends_of_user)
				inter_section_user = set(friends_of_user).intersection(set(user_business))
				# date_user = dt.strptime(date_user,"%Y-%m-%d")
				if len(inter_section_user) !=0:
					for friend in inter_section_user:
					    review_friend_list = review_dict[business_id][friend]
					    for review_friend in review_friend_list:
					    	date_friend = review_friend[1]
					    	# date_friend = dt.strptime(review_friend[1] ,"%Y-%m-%d")
					    if date_user < date_friend:
					    	influence[business_id][user_id] +=1.0/number_review_bz
	return influence
	# print influence
	# with open('inclunce3.json','w') as outfile:
	# 	json.dump(influence, outfile)
def get_incluenc_4():
	#multiply star of the review
	biz_dict = get_biz_dict(biz)
	review_dict, review_dict_user_list = get_review_dict(review_file)
	friend_dict = get_friend_dict(user_file)
	influence =defaultdict(lambda:defaultdict(int))
	for business_id, v in review_dict.iteritems():
		# user_id_list = review_dict[business_id][0]
		# print business_id,len(v)
		# break
		user_business = review_dict_user_list[business_id]
		for user_id, vv in v.iteritems():
			for review in vv:
		# user_id = review_dict[business_id]
				date_user = review[1]

				star_user = review[0]
				friends_of_user = friend_dict[user_id]
				inter_section_user = set(friends_of_user).intersection(set(user_business))
				# date_user = dt.strptime(date_user,"%Y-%m-%d")
				if len(inter_section_user) !=0:
					for friend in inter_section_user:
					    review_friend_list = review_dict[business_id][friend]
					    for review_friend in review_friend_list:
					    	date_friend = review_friend[1]
					    	# date_friend = dt.strptime(review_friend[1] ,"%Y-%m-%d")
					    if date_user < date_friend:
					    	influence[business_id][user_id] +=1.0* star_user
	return influence
	# print influence
	# with open('influnce4.json','w') as outfile:
	# 	json.dump(influence, outfile)
def get_incluenc_5():
	#divide by fans of friends,friends of friends
	biz_dict = get_biz_dict(biz)
	review_dict, review_dict_user_list = get_review_dict(review_file)
	friend_dict = get_friend_dict(user_file)
	fan_dict = get_fandict(user_file)
	influence =defaultdict(lambda:defaultdict(int))
	for business_id, v in review_dict.iteritems():
		# user_id_list = review_dict[business_id][0]
		# print business_id,len(v)
		# break
		user_business = review_dict_user_list[business_id]
		for user_id, vv in v.iteritems():
			for review in vv:
		# user_id = review_dict[business_id]
				date_user = review[1]
				star = review[0]
				friends_of_user = friend_dict[user_id]

				inter_section_user = set(friends_of_user).intersection(set(user_business))
				# date_user = dt.strptime(date_user,"%Y-%m-%d")
				if len(inter_section_user) !=0:
					for friend in inter_section_user:
						# number_of_fan_of_friends = fan_dict[friend]
						# number_of_friends_of_friends = len(friend_dict[friend])
						# n_fan_friends_of_friends = number_of_fan_of_friends + number_of_friends_of_friends
						review_friend_list = review_dict[business_id][friend]
						for review_friend in review_friend_list:
							date_friend = review_friend[1]
							# date_friend = dt.strptime(review_friend[1] ,"%Y-%m-%d")
						if date_user < date_friend:
							number_of_friends_user = len(friends_of_user)
							number_of_fan_user = fan_dict[user_id]
							n_fan_friends_of_user = number_of_friends_user + number_of_fan_user
							influence[business_id][user_id] = n_fan_friends_of_user
	return influence
	# print influence
	# with open('inclunce5.json','w') as outfile:
	# 	json.dump(influence, outfile)
# get_incluenc_5()
# file_list = ["incluence1.json","incluence2.json","incluence3.json","influence4.json","inclunce5.json"]
# for file in file_list:
# 	with open(file) as infile: 
# 		# for line in infile:
# 		json_decode = json.loads(infile)
#         print type(json_decode)
def influence_all():
	incluence1 = get_incluenc_1()
	incluence2 = get_incluenc_2()
	incluence3 = get_incluenc_3()
	incluence4 = get_incluenc_4()
	incluence5 = get_incluenc_5()
	new = defaultdict(lambda:defaultdict(list))
	for k1,v in incluence1.iteritems():
		for k2,vaule in v.iteritems():
			new[k1][k2] = [incluence1[k1][k2],incluence2[k1][k2],incluence3[k1][k2],incluence4[k1][k2], incluence5[k1][k2]]
	with open('inclunce_all.json','w') as outfile:
			json.dump(new, outfile)
def get_first_user_review():
	# biz_dict = get_biz_dict(biz)
	review_dict, review_dict_user_list = get_review_dict(review_file)
	# friend_dict = get_friend_dict(user_file)
	# fan_dict = get_fandict(user_file)
	# influence =defaultdict(lambda:defaultdict(int))
	first_user = defaultdict(str)
	for k1,v in review_dict.iteritems():
		min = dt.strptime("2120-02-02","%Y-%m-%d")
		for k2,v2 in v.iteritems():
			for review in v2:
				if review[1]< min:
					first_user[k1] = k2
			# break
			# if v2[1] < min:
				
	with open('first_user.json','w') as outfile:
			json.dump(first_user, outfile)

	# return first_user

# get_first_user_review()
def weighted_influence():
	incluence1 = get_incluenc_1()
	incluence2 = get_incluenc_2()
	incluence3 = get_incluenc_3()
	incluence4 = get_incluenc_4()
	incluence5 = get_incluenc_5()
	new = defaultdict(lambda:defaultdict(float))
	a1 = 0.5
	a2 = 0.05
	a3 = 0.05
	a4 = 0.3
	a5 = 0.1
	for k1,v in incluence1.iteritems():
		for k2,vaule in v.iteritems():
			new[k1][k2] = a1 * incluence1[k1][k2] + a2* incluence2[k1][k2] + a3* incluence3[k1][k2] + a4 *incluence4[k1][k2] + a5 * incluence5[k1][k2]
	min = 1000000
	max = -100000
	for k,v in new.iteritems():
		for k2,v2 in v.iteritems():
			if v2 < min:
				min = v2
			if v2 > max:
				max = v2
	print min,max,"min,max"
	new_normalize = defaultdict(lambda:defaultdict(float))
	for k,v in new.iteritems():
		for k2,v2 in v.iteritems():
			new_normalize[k1][k2] = (v2-min)/(max - min) *100.0
	with open('normalize_influence.json','w') as outfile:
			json.dump(new_normalize, outfile)

	# print new_normalize

# weighted_influence()

def user_biz_influence():
	incluence1 = get_incluenc_1()
	incluence2 = get_incluenc_2()
	incluence3 = get_incluenc_3()
	incluence4 = get_incluenc_4()
	incluence5 = get_incluenc_5()
	new = defaultdict(lambda:defaultdict(float))
	a1 = 0.5
	a2 = 0.05
	a3 = 0.05
	a4 = 0.3
	a5 = 0.1
	for k1,v in incluence1.iteritems():
		for k2,vaule in v.iteritems():
			new[k1][k2] = a1 * incluence1[k1][k2] + a2* incluence2[k1][k2] + a3* incluence3[k1][k2] + a4 *incluence4[k1][k2] + a5 * incluence5[k1][k2]
	user_influence = defaultdict(float)
	biz_influence = defaultdict(float)
	for k1,v in incluence1.iteritems():
		for k2,value in v.iteritems():
			user_influence[k2] += value
			biz_influence[k1] += value
	print type(user_influence)
	print type(biz_influence)
	# min_user = min(user_influence.iteritems(), key = operator.iteritems(1))[1]
	# max_user = max(user_influence.iteritems(), key = operator.iteritems(1))[1]

	# min_biz = min(biz_influence.iteritems(), key = operator.iteritems(1))[1]
	# max_biz = max(biz_influence.iteritems(), key = operator.iteritems(1))[1]
	min_user = min_biz = 1000000000
	max_user = max_biz = -100000000
	for k,v in user_influence.iteritems():
			if v < min_user:
				min_user = v
			if v > max_user:
				max_user = v
	for k,v in biz_influence.iteritems():
			if v < min_biz:
				min_biz = v
			if v > max_biz:
				max_biz = v
	print min_user,max_user,min_biz,max_biz,"min_user,max_user,min_biz,max_biz"

	user_normalize = defaultdict(float)
	biz_normalize = defaultdict(float)

	for k,v in user_influence.iteritems():
		user_normalize[k] = (v - min_user)/(max_user - min_user) * 100.0
	for k,v in biz_influence.iteritems():
		biz_normalize[k] = (v - min_biz)/(max_biz - min_biz) * 100.0
	# print user_normalize
	# print biz_normalize
	user_sort = sorted(user_normalize.items(), key = operator.itemgetter(1),reverse = True)
	biz_sort = sorted(biz_normalize.items(), key = operator.itemgetter(1), reverse = True)
	# with open('user_influence.json','w') as outfile:
	# 		json.dump(user_sort, outfile)
	# with open('biz_influence.json','w') as outfile:
	# 		json.dump(biz_sort, outfile)
	# print user_sort,"user_sort"
	# print biz_sort,"biz_sort"
	user_sort_100 = user_sort[:100]
	biz_sort_100 = biz_sort[:100]

	with open('user_influence_100.json','w') as outfile:
			json.dump(user_sort_100, outfile)
	with open('biz_influence_100.json','w') as outfile:
			json.dump(biz_sort_100, outfile)
	# print user_sort_100
	# print len(user_sort_100),"len-user"
	# print len(biz_sort),"biz_sort"
# user_biz_influence()
def kevin_data(biz):
	biz_dict = get_biz_dict(biz)
	incluence1 = get_incluenc_1()
	incluence2 = get_incluenc_2()
	incluence3 = get_incluenc_3()
	incluence4 = get_incluenc_4()
	incluence5 = get_incluenc_5()
	new = defaultdict(lambda:defaultdict(float))
	a1 = 0.5
	a2 = 0.05
	a3 = 0.05
	a4 = 0.3
	a5 = 0.1
	for k1,v in incluence1.iteritems():
		for k2,vaule in v.iteritems():
			new[k1][k2] = a1 * incluence1[k1][k2] + a2* incluence2[k1][k2] + a3* incluence3[k1][k2] + a4 *incluence4[k1][k2] + a5 * incluence5[k1][k2]
	user_influence = defaultdict(float)
	biz_influence = defaultdict(float)
	for k1,v in incluence1.iteritems():
		for k2,value in v.iteritems():
			user_influence[k2] += value
			biz_influence[k1] += value
	print type(user_influence)
	print type(biz_influence)
	# min_user = min(user_influence.iteritems(), key = operator.iteritems(1))[1]
	# max_user = max(user_influence.iteritems(), key = operator.iteritems(1))[1]

	# min_biz = min(biz_influence.iteritems(), key = operator.iteritems(1))[1]
	# max_biz = max(biz_influence.iteritems(), key = operator.iteritems(1))[1]
	min_user = min_biz = 1000000000
	max_user = max_biz = -100000000
	for k,v in user_influence.iteritems():
			if v < min_user:
				min_user = v
			if v > max_user:
				max_user = v
	for k,v in biz_influence.iteritems():
			if v < min_biz:
				min_biz = v
			if v > max_biz:
				max_biz = v
	print min_user,max_user,min_biz,max_biz,"min_user,max_user,min_biz,max_biz"

	user_normalize = defaultdict(float)
	biz_normalize = defaultdict(float)

	for k,v in user_influence.iteritems():
		user_normalize[k] = (v - min_user)/(max_user - min_user) * 100.0
	for k,v in biz_influence.iteritems():
		biz_normalize[k] = (v - min_biz)/(max_biz - min_biz) * 100.0
	# print user_normalize
	# print biz_normalize
	user_sort = sorted(user_normalize.items(), key = operator.itemgetter(1),reverse = True)
	biz_sort = sorted(biz_normalize.items(), key = operator.itemgetter(1), reverse = True)
	# with open('user_influence.json','w') as outfile:
	# 		json.dump(user_sort, outfile)
	# with open('biz_influence.json','w') as outfile:
	# 		json.dump(biz_sort, outfile)
	# print user_sort,"user_sort"
	# print biz_sort,"biz_sort"
	# user_sort_100 = user_sort[:100]
	# biz_sort_100 = biz_sort[:100]
	new_dict = {}
	new_dict["data"] = []
	for biz in biz_sort:
		id = biz[0]
		weight = biz[1]
		lat = biz_dict[id][1]
		longti = biz_dict[id][0]
		inside_dict = {}
		inside_dict["weight"] = weight
		inside_dict["lat"] = lat
		inside_dict["long"] = longti
		new_dict["data"].append(inside_dict)
	# print new_dict
	with open('kevin_biz.json','w') as outfile:
			json.dump(new_dict, outfile)
kevin_data(biz)
	# min = 1000000000000000
	# max = -100000000000000

	# for k,v in new.iteritems():
	# 	for k2,v2 in v.iteritems():
	# 		if v2 < min:
	# 			min = v2
	# 		if v2 > max:
	# 			max = v2

	# print min,max,"min,max"
	# new_normalize = defaultdict(lambda:defaultdict(float))
	# for k,v in new.iteritems():
	# 	for k2,v2 in v.iteritems():
	# 		new_normalize[k1][k2] = (v2-min)/(max - min) *100.0



# print new
# print review_dict,'review_dict'
# print biz_dict,'biz_dict'
# print friend_dict,'friend_dict'