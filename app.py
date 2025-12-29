"""
전기차 배터리 열폭주 방지필름 시장 조사 대시보드 서버
Flask를 사용하여 HTML 대시보드와 뉴스 JSON 데이터를 서빙합니다.
"""

from flask import Flask, render_template, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
import sys
from datetime import datetime

# Flask 앱 초기화 - 템플릿 경로 명시
app = Flask(__name__, template_folder='templates', static_folder=None)
CORS(app)  # CORS 문제 해결

# 라우트는 아래에서 정의됨


@app.route('/')
def index():
    """메인 대시보드 페이지"""
    try:
        # 템플릿 파일 경로 확인
        template_path = os.path.join('templates', 'index.html')
        if not os.path.exists(template_path):
            return jsonify({
                "error": "Template not found",
                "message": f"템플릿 파일을 찾을 수 없습니다: {template_path}",
                "current_dir": os.getcwd(),
                "files": os.listdir('.') if os.path.exists('.') else []
            }), 500
        
        return render_template('index.html')
    except Exception as e:
        import traceback
        return jsonify({
            "error": "Template rendering error",
            "message": str(e),
            "traceback": traceback.format_exc()
        }), 500


@app.route('/api/news')
def get_news():
    """뉴스 데이터 API 엔드포인트"""
    try:
        if os.path.exists('news_data.json'):
            with open('news_data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            return jsonify(data)
        else:
            return jsonify({
                "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "total_articles": 0,
                "articles": []
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/refresh', methods=['GET', 'POST'])
def refresh_news():
    """뉴스 데이터 새로고침 (크롤러 직접 호출)"""
    try:
        # subprocess 대신 직접 함수 호출
        from crawler import main as crawl_main
        
        # 크롤러 실행 (타임아웃 60초)
        import signal
        
        def timeout_handler(signum, frame):
            raise TimeoutError("크롤링이 60초를 초과했습니다.")
        
        # 크롤러 실행
        try:
            result = crawl_main()
        except Exception as crawl_error:
            # 크롤링 실패해도 기존 데이터가 있으면 유지
            if os.path.exists('news_data.json'):
                with open('news_data.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return jsonify({
                    "success": False,
                    "message": f"크롤링 중 오류가 발생했습니다: {str(crawl_error)}. 기존 데이터를 유지합니다.",
                    "total_articles": data.get('total_articles', 0),
                    "error": str(crawl_error)
                }), 500
            else:
                raise
        
        # 결과 확인
        if os.path.exists('news_data.json'):
            with open('news_data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            message = f"뉴스 데이터가 성공적으로 업데이트되었습니다. ({data.get('total_articles', 0)}개 기사)"
            if data.get('errors'):
                message += f" (일부 오류 발생: {len(data.get('errors', []))}개)"
            
            return jsonify({
                "success": True,
                "message": message,
                "total_articles": data.get('total_articles', 0),
                "errors": data.get('errors')
            })
        else:
            return jsonify({
                "success": False,
                "message": "크롤링은 완료되었지만 데이터 파일을 찾을 수 없습니다."
            }), 500
            
    except ImportError as e:
        return jsonify({
            "success": False,
            "message": f"크롤러 모듈을 불러올 수 없습니다: {str(e)}"
        }), 500
    except TimeoutError as e:
        return jsonify({
            "success": False,
            "message": f"크롤링 시간 초과: {str(e)}"
        }), 500
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        # 사용자에게는 간단한 메시지만 전달
        return jsonify({
            "success": False,
            "message": f"크롤링 중 오류 발생: {str(e)}",
            "detail": error_detail if app.debug else None
        }), 500


# 에러 핸들러 추가 - 모든 404를 JSON으로 반환
@app.errorhandler(404)
def not_found(error):
    # 요청 경로 확인
    from flask import request
    # 실제 등록된 라우트 목록 가져오기
    available_routes = []
    try:
        for rule in app.url_map.iter_rules():
            if rule.endpoint not in ['static']:
                available_routes.append(str(rule))
    except:
        available_routes = ["/", "/api/news", "/api/refresh", "/health", "/api/routes"]
    
    return jsonify({
        "error": "Not found", 
        "message": f"요청한 리소스를 찾을 수 없습니다: {request.path}",
        "available_routes": available_routes,
        "method": request.method
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error", "message": "서버 내부 오류가 발생했습니다."}), 500

# 루트 경로 테스트
@app.route('/health')
def health():
    """헬스 체크 엔드포인트"""
    from flask import request
    return jsonify({
        "status": "ok",
        "templates_exists": os.path.exists('templates'),
        "index_exists": os.path.exists('templates/index.html') if os.path.exists('templates') else False,
        "routes": [str(rule) for rule in app.url_map.iter_rules()],
        "current_path": request.path
    })

# 디버깅용: 모든 라우트 확인
@app.route('/api/routes', methods=['GET'])
def list_routes():
    """등록된 모든 라우트 확인"""
    try:
        routes = []
        for rule in app.url_map.iter_rules():
            # static과 error 핸들러 제외
            if rule.endpoint not in ['static']:
                routes.append({
                    "endpoint": rule.endpoint,
                    "methods": list(rule.methods),
                    "path": str(rule)
                })
        return jsonify({
            "status": "ok",
            "total_routes": len(routes),
            "routes": routes
        })
    except Exception as e:
        return jsonify({
            "error": str(e),
            "message": "라우트 정보를 가져오는 중 오류가 발생했습니다."
        }), 500

# 앱 시작 시 라우트 확인 (모든 라우트 등록 후)
def print_routes():
    """등록된 라우트 출력"""
    print("=" * 60)
    print("등록된 라우트:")
    print("-" * 60)
    for rule in app.url_map.iter_rules():
        if rule.endpoint not in ['static']:
            methods = ', '.join(sorted(rule.methods - {'HEAD', 'OPTIONS'}))
            print(f"  {methods:15s} {str(rule):30s} -> {rule.endpoint}")
    print("=" * 60)

if __name__ == '__main__':
    # templates 폴더가 없으면 생성
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    # 라우트 출력
    print_routes()
    
    # Render.com에서는 PORT 환경 변수를 사용
    port = int(os.environ.get('PORT', 5000))
    
    print(f"\n서버를 시작합니다...")
    print(f"대시보드: http://localhost:{port}")
    print(f"템플릿 폴더 존재: {os.path.exists('templates')}")
    print(f"index.html 존재: {os.path.exists('templates/index.html') if os.path.exists('templates') else False}\n")
    
    app.run(debug=False, host='0.0.0.0', port=port)
else:
    # gunicorn으로 실행될 때도 라우트 출력
    # 앱 컨텍스트 내에서만 라우트 출력 가능
    try:
        with app.app_context():
            print_routes()
    except:
        print("앱 컨텍스트 없이 라우트를 출력할 수 없습니다. 앱이 로드된 후 확인하세요.")

