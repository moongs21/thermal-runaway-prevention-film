"""
WSGI 진입점 - Render.com 배포용
gunicorn이 이 파일을 통해 앱을 로드합니다.
"""
import os
import sys

# 현재 디렉토리를 Python 경로에 추가
sys.path.insert(0, os.path.dirname(__file__))

# 앱 임포트
from app import app

# 앱이 제대로 로드되었는지 확인
if app is None:
    raise RuntimeError("앱을 로드할 수 없습니다!")

# 라우트 확인
print("=" * 60)
print("WSGI 진입점에서 앱 로드 완료")
print("=" * 60)
try:
    with app.app_context():
        print("등록된 라우트:")
        for rule in app.url_map.iter_rules():
            if rule.endpoint not in ['static']:
                methods = ', '.join(sorted(rule.methods - {'HEAD', 'OPTIONS'}))
                print(f"  {methods:15s} {str(rule):30s} -> {rule.endpoint}")
except Exception as e:
    print(f"라우트 확인 중 오류: {e}")
print("=" * 60)

# 앱 객체를 명시적으로 export (gunicorn이 application을 찾을 수도 있음)
application = app

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
