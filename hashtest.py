from werkzeug.security import generate_password_hash, check_password_hash

# 실제 저장된 해시 (비밀번호: 'pohang')
PASSWORD_HASH = generate_password_hash('pohang')

# 사용자 입력 (문자열 그대로 받아야 함)
password = input('비밀번호: ')

print(PASSWORD_HASH,"------------")
print(password)
# 입력값과 해시 비교
if check_password_hash(PASSWORD_HASH, password):
    print("통과")
else:
    print("틀림")
