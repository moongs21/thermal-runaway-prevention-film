"""
전기차 배터리 열폭주 방지필름 관련 최신 뉴스 크롤러
RSS 피드와 간단한 웹 스크래핑을 결합하여 안정적으로 뉴스 데이터를 수집합니다.
"""

import json
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import feedparser
import time
import re


def crawl_google_news_rss(keyword, max_results=5):
    """구글 뉴스 RSS 피드에서 뉴스 수집 (더 안정적)"""
    news_items = []
    
    try:
        # 구글 뉴스 RSS URL
        rss_url = f"https://news.google.com/rss/search?q={keyword}&hl=ko&gl=KR&ceid=KR:ko"
        
        # RSS 피드 파싱
        feed = feedparser.parse(rss_url)
        
        for entry in feed.entries[:max_results]:
            try:
                title = entry.get('title', '').strip()
                link = entry.get('link', '')
                
                # 날짜 파싱
                date_str = datetime.now().strftime("%Y-%m-%d")
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    date_str = datetime(*entry.published_parsed[:6]).strftime("%Y-%m-%d")
                
                # 요약 추출
                snippet = ""
                if hasattr(entry, 'summary'):
                    snippet = entry.summary
                elif hasattr(entry, 'description'):
                    snippet = entry.description
                
                # HTML 태그 제거
                if snippet:
                    soup = BeautifulSoup(snippet, 'html.parser')
                    snippet = soup.get_text().strip()[:200]
                
                # 매체명 추출
                source = "Google News"
                if hasattr(entry, 'source'):
                    source = entry.source.get('title', 'Google News')
                
                if title and link:
                    news_items.append({
                        "title": title,
                        "source": source,
                        "date": date_str,
                        "snippet": snippet,
                        "link": link
                    })
            except Exception as e:
                print(f"RSS 항목 처리 중 오류: {e}")
                continue
                
    except Exception as e:
        print(f"구글 뉴스 RSS 크롤링 오류 ({keyword}): {e}")
    
    return news_items


def crawl_with_requests(keyword, max_results=3):
    """requests와 BeautifulSoup을 사용한 간단한 크롤링 (대체 방법)"""
    news_items = []
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # 구글 뉴스 검색 URL
        search_url = f"https://www.google.com/search?q={keyword}&tbm=nws&hl=ko"
        
        response = requests.get(search_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 뉴스 결과 찾기
        news_divs = soup.find_all('div', class_='g', limit=max_results)
        
        for div in news_divs:
            try:
                # 제목 추출
                title_elem = div.find('h3')
                if not title_elem:
                    continue
                title = title_elem.get_text().strip()
                
                # 링크 추출
                link_elem = div.find('a')
                if not link_elem or not link_elem.get('href'):
                    continue
                
                link = link_elem['href']
                if link.startswith('/url?q='):
                    link = link.split('/url?q=')[1].split('&')[0]
                
                # 요약 추출
                snippet_elem = div.find('div', {'data-sncf': True}) or div.find('span', class_='st')
                snippet = snippet_elem.get_text().strip()[:200] if snippet_elem else ""
                
                # 매체명 추출
                source = "Google News"
                source_elem = div.find('span')
                if source_elem:
                    source_text = source_elem.get_text()
                    if '·' in source_text:
                        source = source_text.split('·')[0].strip()
                
                if title and link:
                    news_items.append({
                        "title": title,
                        "source": source,
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "snippet": snippet,
                        "link": link
                    })
            except Exception as e:
                print(f"뉴스 항목 처리 중 오류: {e}")
                continue
                
    except Exception as e:
        print(f"requests 크롤링 오류 ({keyword}): {e}")
    
    return news_items


def main():
    """메인 크롤링 함수"""
    print("뉴스 크롤링을 시작합니다...")
    
    keywords = [
        "전기차 배터리 열폭주 방지",
        "Battery Thermal Runaway Prevention",
        "Mica vs Aerogel EV Battery",
        "LG Chem Safety Reinforced Layer",
        "배터리 화재 방지 필름"
    ]
    
    all_news = []
    
    # RSS 피드 방식으로 크롤링 시도
    for keyword in keywords:
        print(f"키워드 검색 중 (RSS): {keyword}")
        news = crawl_google_news_rss(keyword, max_results=3)
        all_news.extend(news)
        time.sleep(1)  # 요청 간 딜레이
    
    # RSS로 충분한 결과를 얻지 못한 경우 requests 방식으로 보완
    if len(all_news) < 10:
        print("RSS 결과가 부족하여 requests 방식으로 보완합니다...")
        for keyword in keywords[:2]:  # 처음 2개 키워드만
            news = crawl_with_requests(keyword, max_results=2)
            all_news.extend(news)
            time.sleep(2)
    
    # 중복 제거 (제목 기준)
    seen_titles = set()
    unique_news = []
    for item in all_news:
        title_lower = item["title"].lower()
        if title_lower not in seen_titles:
            seen_titles.add(title_lower)
            unique_news.append(item)
    
    # 최신순 정렬 (날짜 기준)
    unique_news.sort(key=lambda x: x["date"], reverse=True)
    
    # 최대 15개로 제한
    unique_news = unique_news[:15]
    
    # JSON 파일로 저장
    output_data = {
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_articles": len(unique_news),
        "articles": unique_news
    }
    
    with open("news_data.json", "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"총 {len(unique_news)}개의 뉴스를 수집하여 news_data.json에 저장했습니다.")
    return unique_news


if __name__ == "__main__":
    main()

