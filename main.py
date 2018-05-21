import requests
import json
import os
import random
from time import sleep

RESULTS = 'orders.txt' # Text file where orders are located in email:ordernumber format
DELAY = 0 # Delay in seconds between checking orders
PROXY_FILE = 'proxies.txt' # Text file where proxies are located in ip:host or ip:host:user:pass format
DISPLAY = False # Whether or not you want the full output saved to RESULTS to be displayed in terminal as well
REGION =  'en-us' # Full list of regions can be found in regions.txt
REMOVE_CANCELLED = False # Choose whether or not you want cancelled orders removed from RESULTS
DELIMITER = ' | ' # Choose how values are separated in RESULTS

WIDTH = 30 # Don't touch

def center(string, spacer):
	count = ((WIDTH - len(string)) / 2)
	if count > 0:
		return (count - 1) * spacer + ' ' + string + ' ' + (count - 1) * spacer
	else:
		return string

def header():
	if os.name == 'nt':
		os.system('cls')
	else:
		os.system('clear')
	print center('Nike Order Checker', '~')
	print center('Made by @DefNotAvg', '~')
	print ''

def smart_sleep(DELAY):
	for a in xrange (DELAY, 0, -1):
		print 'Sleeping for {} seconds...\r'.format(str(a)),
		sleep(1)
	print 'Sleeping for {} seconds complete!'.format(str(DELAY))

def set_proxy(PROXIES):
	if PROXIES != []:
		proxy = random.choice(PROXIES)
		proxies = {
		  'http': 'http://{}'.format(proxy),
		  'https': 'http://{}'.format(proxy),
		}
	else:
		proxies = {
		  'http': None,
		  'https': None,
		}
	return proxies

def smart_split(item):
	if ':' in item:
		return item.split(':')
	else:
		return item.split(DELIMITER)

header()
with open(RESULTS, 'r') as myfile:
	text = myfile.read()
info = list(set([item for item in text.split('\n') if item != '' and len([field for field in smart_split(item) if item != '']) > 1]))
statuses = []
if len(info) > 0:
	print center('Gathering order status for {} orders...\n'.format(str(len(info))), ' ')
else:
	print center('No orders found in {}'.format(RESULTS), ' ')
sleep(1)
try:
	with open(PROXY_FILE, 'r') as myfile:
		PROXIES = ['{}:{}@{}:{}'.format(PROXY.split(':')[2], PROXY.split(':')[3], PROXY.split(':')[0], PROXY.split(':')[1]) if PROXY != '' and PROXY.count(':') == 3 else PROXY for PROXY in myfile.read().split('\n') if PROXY != '']
except:
	with open(PROXY_FILE, 'w') as myfile:
		PROXIES = myfile.write('')
	PROXIES = []
if PROXIES == []:
	proxies = set_proxy(PROXIES)
for i in range(0,len(info)):
	header()
	line = info[i]
	order = smart_split(line)
	email = order[0]
	order_number = order[1]
	print '[{}/{}] Gathering order status...'.format(str(i + 1), str(len(info)))
	if PROXIES != []:
		proxies = set_proxy(PROXIES)
	session = requests.Session()
	headers = {
	    'origin': 'https://secure-store.nike.com',
	    'accept-encoding': 'gzip, deflate, br',
	    'accept-language': '{}-{},en;q=0.9'.format(REGION.split('-')[0].lower(), REGION.split('-')[1].upper()),
	    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
	    'content-type': 'application/x-www-form-urlencoded',
	    'accept': '*/*',
	    'referer': 'https://secure-store.nike.com/common/content/endpoint.html',
	    'authority': 'secure-store.nike.com',
	    'x-requested-with': 'XMLHttpRequest',
	}
	data = [
	  ('action', 'getAnonymousOrderDetails'),
	  ('lang_locale', '{}_{}'.format(REGION.split('-')[0].lower(), REGION.split('-')[1].upper())),
	  ('country', '{}'.format(REGION.split('-')[1].upper())),
	  ('endpoint', 'getAnonymousOrderDetails'),
	  ('orderId', order_number),
	  ('email', email),
	  ('deviceType', 'desktop'),
	]
	try:
		response = session.post('https://secure-store.nike.com/nikestore/html/services/orders/orderDetails', headers=headers, data=data, proxies=proxies)
		content = json.loads(response.content)
	except:
		status = 'Error getting order status'
	try:
		status = content['data']['order']['shippingGroups'][0]['status']
	except:
		try:
			status = content['data']['order']['status']
		except:
			status = 'Error getting order status'
	try:
		name = '{} - {}'.format(content['data']['order']['shippingGroups'][0]['commerceItems'][0]['product']['name'], content['data']['order']['shippingGroups'][0]['commerceItems'][0]['displaySize'])
	except:
		name = '' 
	if status == 'Shipped':
		try:
			status = content['data']['order']['shippingGroups'][0]['status']
			if status != 'Delivered':
				try:
					tracking_number = content['data']['order']['shippingGroups'][0]['trackingNumber']
				except:
					tracking_number = ''
				try:
					expected_delivery = content['data']['order']['shippingGroups'][0]['commerceItems'][0]['expectedDeliveryDate']
				except:
					expected_delivery = ''
		except:
			tracking_number = 'Error getting tracking number'
			expected_delivery = ''
	else:
		tracking_number = ''
		expected_delivery = ''
	try:
		first_name = content['data']['order']['shippingGroups'][0]['shippingAddress']['firstName']
	except:
		first_name = ''
	try:
		last_name = content['data']['order']['shippingGroups'][0]['shippingAddress']['lastName']
	except:
		last_name = ''
	try:
		address1 = content['data']['order']['shippingGroups'][0]['shippingAddress']['address1']
	except:
		address1 = ''
	try:
		address2 = content['data']['order']['shippingGroups'][0]['shippingAddress']['address2']
	except:
		address2 = ''
	try:
		city = content['data']['order']['shippingGroups'][0]['shippingAddress']['city']
	except:
		city = ''
	try:
		state = content['data']['order']['shippingGroups'][0]['shippingAddress']['state']
	except:
		state = ''
	try:
		zip_code = content['data']['order']['shippingGroups'][0]['shippingAddress']['postalCode']
	except:
		zip_code = ''
	statuses.append(status)
	if name != '':
		if len(order) > 2:
			order[2] = name
			final = DELIMITER.join(order[:3])
		else:
			order.append(name)
			final = DELIMITER.join(order[:3])
	if first_name != '' and last_name != '' and address1 != '' and address2 != '' and city != '' and state != '' and zip_code != '':
		if address2 != None:
			address = '{} {} {} {} {}, {} {}'.format(first_name, last_name, address1, address2, city, state, zip_code)
		else:
			address = '{} {} {} {}, {} {}'.format(first_name, last_name, address1, city, state, zip_code)
		if len(order) > 3:
			order[3] = address
			final = DELIMITER.join(order[:4])
		else:
			order.append(address)
			final = DELIMITER.join(order[:4])	
	if len(order) > 4:
		order[4] = status
		final = DELIMITER.join(order[:5])
	else:
		order.append(status)
		final = DELIMITER.join(order[:5])
	if tracking_number != '':
		if len(order) > 5:
			order[5] = tracking_number
			final = DELIMITER.join(order[:6])
		else:
			order.append(tracking_number)
			final = DELIMITER.join(order[:6])
	if expected_delivery != '':
		if len(order) > 6:
			order[6] = expected_delivery
			final = DELIMITER.join(order[:7])
		else:
			order.append(expected_delivery)
			final = DELIMITER.join(order[:7])
	with open(RESULTS, 'r') as myfile:
		text = myfile.read()
	with open(RESULTS, 'w') as myfile:
			myfile.write(text.replace(line, final))
	if DELAY > 0 and i != len(info) - 1:
		print 'Order {}: {}\n'.format(order_number, status)
		smart_sleep(DELAY)
if len(info) > 0:
	header()
	with open(RESULTS, 'r') as myfile:
		text = myfile.read()
	info = [item for item in text.split('\n') if item != '' and len([field for field in smart_split(item) if item != '']) > 1]
	display_text = ''
	result_text = ''
	sorted_list = sorted(list(set(statuses)))
	for category in sorted_list:
		display_text += category + '\n'
		for item in info:
			if smart_split(item)[4] == category:
				display_text += '\n' + item
		display_text += '\n\n'
		if category != 'Cancelled' or not REMOVE_CANCELLED:
			result_text += category + '\n'
			for item in info:
				if smart_split(item)[4] == category:
					result_text += '\n' + item
			if sorted_list.index(category) != len(sorted_list) - 1:
				result_text += '\n\n'
	for category in sorted_list:
		result_text = result_text.replace(DELIMITER + category, '')
	with open(RESULTS, 'w') as myfile:
		myfile.write(result_text)
	if DISPLAY:
		for category in sorted_list:
			display_text = display_text.replace(DELIMITER + category, '')
		print display_text
	print center('Output', '~')
	print ''
	for category in sorted(list(set(statuses))):
		print center('{}: {}'.format(category, str(sum(category == status for status in statuses))), ' ')
	raw_input('\n' + WIDTH * '~' + '\n\n' + center('Output saved to {}'.format(RESULTS), ' ') + '\n\n' + center('Press enter to quit', ' '))
else:
	raw_input('\n' + center('Press enter to quit', ' '))

quit()