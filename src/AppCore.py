import json
import os
import tempfile
import shutil

class AppCore:
    """
    AppCore 클래스는 통합적으로 여러 프로그램의 핵심 시스템 기능을 제공합니다.

    JSON 파일 관리, 다국어 지원, 자료 구조 검색 등 
    대부분의 프로그램에 적용 가능한 핵심 시스템 기능을 제공합니다.
    """
    def __init__(self):
        self.config = self.load_json("data/config.json")
        self.lang = [os.path.splitext(file)[0] for file in os.listdir("./language")]
        self._lang_cache = {}  # 언어 캐시 딕셔너리


    def load_json(self, file_path):
        """
        json 파일을 딕셔너리로 불러오는 함수

        실패 시 False 반환, 성공 시 딕셔너리 반환

        Args:
            file_path (str): 불러올 파일 경로
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading JSON from {file_path}: {e}")
            return False

    def save_json(self, data, file_path, key=None):
        """
        딕셔너리를 json 파일로 저장하는 함수 (원자적 쓰기 적용)

        실패 시 False 반환, 성공 시 True 반환

        Args:
            data (dict): 저장할 데이터
            file_path (str): 저장할 파일 경로
            key (str): 저장할 데이터의 키 (선택적)
        """
        # 디렉토리가 존재하지 않으면 생성
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        temp_file_path = None  # 임시 파일 경로 초기화
        try:
            # 저장할 최종 데이터 준비
            if key is not None:
                # key가 None이 아닌 경우 기존 데이터에 추가
                if os.path.exists(file_path):
                    existing_data = self.load_json(file_path)
                    if existing_data is False:
                        raise ValueError(f"Failed to load existing JSON file: {file_path}")
                else:
                    existing_data = {}
                
                existing_data[key] = data
                final_data = existing_data
            else:
                # key가 None인 경우 전체 데이터를 덮어쓰기
                final_data = data
            
            # 원자적 쓰기: 임시 파일에 먼저 쓰기
            with tempfile.NamedTemporaryFile(
                mode='w', 
                delete=False, 
                encoding='utf-8', 
                dir=os.path.dirname(file_path), 
                prefix=os.path.basename(file_path) + '.tmp.'
            ) as tmp:
                json.dump(final_data, tmp, indent=4, ensure_ascii=False)
                temp_file_path = tmp.name
            
            # 원자적 이동
            shutil.move(temp_file_path, file_path)
            return True
            
        except Exception as e:
            print(f"Error saving JSON to {file_path}: {e}")
            # 임시 파일 정리 (이동 실패 시)
            if temp_file_path and os.path.exists(temp_file_path):
                try:
                    os.unlink(temp_file_path)
                except OSError:
                    pass
            return False

    def find_keys_by_value(self, json_data, threshold, comparison_type):
        """
        딕셔너리에서 특정 값 이상을 가진 키들을 찾는 함수

        Args:
            comparison_type (str): 비교 유형 ("above", "below", "equal")
            threshold (int or float): 기준 값 (equal의 경우 Any)
            json_data (dict): 딕셔너리 데이터

        Returns:
            List[str]: 조건을 만족하는 키들의 리스트
        """
        matching_keys = []
        comparison_type = comparison_type.lower()

        if comparison_type == "above":
            for key, value in json_data.items():
                if isinstance(value, (int, float)) and value > threshold:
                    matching_keys.append(key)
            return matching_keys
        elif comparison_type == "below":
            for key, value in json_data.items():
                if isinstance(value, (int, float)) and value < threshold:
                    matching_keys.append(key)
            return matching_keys
        elif comparison_type == "equal":
            for key, value in json_data.items():
                if value == threshold:
                    matching_keys.append(key)
            return matching_keys
        return matching_keys

    def text(self, lang, key):
        """
        언어 설정에 따라 텍스트를 반환하는 함수

        Args:
            lang (str): 언어 설정
            key (str): 텍스트 키
        """
        if lang not in self.lang:
            raise ValueError(f"Language '{lang}' not supported. Available languages: {self.lang}")

        # 캐시 확인
        if lang not in self._lang_cache:
            lang_data = self.load_json(f"./language/{lang}.json")
            if lang_data is False:
                raise FileNotFoundError(f"Language file for '{lang}' could not be loaded.")
            self._lang_cache[lang] = lang_data

        # 텍스트 반환
        if key in self._lang_cache[lang]:
            return self._lang_cache[lang][key]
        else:
            raise KeyError(f"Key '{key}' not found in language '{lang}'. Available keys: {list(self._lang_cache[lang].keys())}")
                
    def clear_screen(self):
        """
        화면을 지우는 함수
        플랫폼 독립적이고 안전한 방법을 사용합니다.
        """
        import subprocess
        
        try:
            if os.name == 'nt':  # Windows
                subprocess.run('cls', shell=True, check=True)
            else:  # Unix/Linux/macOS
                subprocess.run('clear', shell=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            # 명령어 실행 실패 시 대체
            print('\n' * 50)