d = [{'k':1}]

print(d[0]['k'])

profile = Profile.objects.raw(
			'''
			SELECT * FROM user_profile_profile 

			WITH hierarchy AS (
				SELECT t.id,
						t.user,
						t.full_name
						t.sponsor
					FROM user_profile_profile t
				WHERE t.sponsor = {own_profile}
				UNION ALL
				SELECT x.id,
						x.user,
						x.full_name
						x.sponsor
						
					FROM user_profile_profile x
					JOIN hierarchy y ON y.user = x.sponsor
				)

				SELECT *
				FROM hierarchy s

			
			''')