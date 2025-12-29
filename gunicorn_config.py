"""
Gunicorn 설정 파일
Render.com 배포를 위한 설정
"""

import os
import multiprocessing

# 바인드 주소 및 포트
bind = f"0.0.0.0:{os.environ.get('PORT', '5000')}"

# 워커 프로세스 수
workers = multiprocessing.cpu_count() * 2 + 1

# 워커 타입
worker_class = "sync"

# 타임아웃 설정
timeout = 120
keepalive = 5

# 로그 설정
accesslog = "-"
errorlog = "-"
loglevel = "info"

# 프로세스 이름
proc_name = "battery-thermal-dashboard"

