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

app = Flask(__name__)
CORS(app)  # CORS 문제 해결


@app.route('/')
def index():
    """메인 대시보드 페이지"""
    return render_template('index.html')


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


@app.route('/api/refresh')
def refresh_news():
    """뉴스 데이터 새로고침 (크롤러 직접 호출)"""
    try:
        # subprocess 대신 직접 함수 호출
        from crawler import main as crawl_main
        
        # 크롤러 실행
        crawl_main()
        
        # 결과 확인
        if os.path.exists('news_data.json'):
            with open('news_data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            return jsonify({
                "success": True,
                "message": f"뉴스 데이터가 성공적으로 업데이트되었습니다. ({data.get('total_articles', 0)}개 기사)",
                "total_articles": data.get('total_articles', 0)
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
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        return jsonify({
            "success": False,
            "message": f"크롤링 중 오류 발생: {str(e)}",
            "detail": error_detail
        }), 500


if __name__ == '__main__':
    # templates 폴더가 없으면 생성
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    print("서버를 시작합니다...")
    print("대시보드: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)

