import jwt
from django.contrib.auth import authenticate


class jwtWrapper():
	secret = 'qwertyuiopasdfghjklzxcvbnm123456';

	def create(self):

		payload = {
			"iss": "Sleep Diary",
			"aud": "www.sleepdiary.io",
			"sub": "contact@sleepdiary.io",
			"Role": [
				"Manager",
				"Project Administrator"
			]
		}
		encoded = jwt.encode(
			payload,
			self.secret,
			algorithm='HS256'
		)

		return encoded

	def check(self, meta):
		parts = meta.split();

		if parts[0].lower() != 'bearer':
			return {'code': 'invalid_header', 'description': 'Authorization header must start with Bearer'}
		elif len(parts) == 1:
			return {'code': 'invalid_header', 'description': 'Token not found'}
		elif len(parts) > 2:
			return {'code': 'invalid_header', 'description': 'Authorization header must be Bearer + \s + token'}

		token = parts[1]

		try:
			payload = jwt.decode(
				token,
				'qwertyuiopasdfghjklzxcvbnm123456',
				audience='www.sleepdiary.io'
			)
		except jwt.ExpiredSignature:
			return authenticate({'code': 'token_expired', 'description': 'token is expired'})
		except jwt.InvalidAudienceError:
			return authenticate(
				{'code': 'invalid_audience', 'description': 'incorrect audience, expected: YOUR_CLIENT_ID'})
		except jwt.DecodeError:
			return authenticate({'code': 'token_invalid_signature', 'description': 'token signature is invalid'})

		# if we get this point means token is verified
		return 1
