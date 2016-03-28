
GET:
path: /calendar/year/2016
- Requires a base64 (user + password) in headers. Uses BASIC AUTH => must be changed later to OAUTH! 
- Returns calendar data for the registered user. User is implicitly taken from the request headers. 
- Returned data comes in a JSON with the following structure:
	{
	"2016-02-02": {
		"sleepingQuality": "regular"
		"tirednessFeeling": "good"
		"date": "2016-02-02T00:28:15.416275Z"
		"user": 1
		"uuid": "6a7e98f0-b49f-32c2-9953-fe55302e83aa"
		}
	};  

POST:
path: /calendar
payload (form data)

date: isoDate ex: 2016-03-27T22:00:00.000Z
userId: int ex 1
sleepingQuality:[good | regular | bad]
tirednessFeeling:[good | regular | bad]

- Requires base64 (user + password) in headers to create user-specific new data. BASIC AUTH. 
- Expects the following values in the payload:
	- <tirednessFeeling>: good | bad | regular
	- <sleepingQuality>: good | bad | regular
	- <date>: ISO format. 
- Response includes a JSON which includes the newly created data with 201 status code. 

PUT:
path: /calendar
paylod (form data)

date: isoDate ex: 2016-03-27T22:00:00.000Z
userId: int ex 1
uuid: hasg md5
sleepingQuality:[good | regular | bad]
tirednessFeeling:[good | regular | bad]

- Requires base64 (user + password) in headers since data can only be modified by users who own it. BASIC AUTH. 
- Expects the following values in the payload:
	- <tirednessFeeling>: good | bad | regular
	- <sleepingQuality>: good | bad | regular
	- <uuid>: uuid value. 
- Response includes a JSON which includes the updated data with 200 status code. 


DELETE:
path /calendar
- 