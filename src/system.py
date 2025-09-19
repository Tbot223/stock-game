import json
import os

class system:
    """
    게임의 전체적인 시스템 클래스

    JSON 파일 관리, 다국어 지원, 자료 구조 검색 등 
    게임의 핵심 시스템 기능을 제공합니다.
    """
    def __init__(self):
        self.config = self.load_json("data/config.json")
        
        self.lang = [os.path.splitext(file)[0] for file in os.listdir("./language")]

    def load_json(self, file_path):
        """
        json 파일을 딕셔너리로 불러오는 함수

        Args:
            file_path (str): 불러올 파일 경로
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_json(self, data, file_path, key=None):
        """
        딕셔너리를 json 파일로 저장하는 함수

        Args:
            data (dict): 저장할 데이터
            file_path (str): 저장할 파일 경로
            key (str): 저장할 데이터의 키 (선택적)
        """
        if key is not None:
            # key가 None이 아닌 경우 기존 데이터에 추가
            with open(file_path, 'r+', encoding='utf-8') as f:
                existing_data = json.load(f)
                existing_data[key] = data
                f.seek(0)
                json.dump(existing_data, f, indent=4)
                f.truncate()
        else:
            # key가 None인 경우 전체 데이터를 덮어쓰기
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)

    def find_key_with_value_above(self, json_data, threshold):
        """
        딕셔너리에서 특정 값 이상을 가진 키들을 찾는 함수

        Args:
            json_data (dict): 딕셔너리 데이터
            threshold (int or float): 기준 값

        Returns:
            list: 기준 값 이상을 가진 키들
        """
        matching_keys = []

        for key, value in json_data.items():
            if isinstance(value, (int, float)) and value > threshold:
                matching_keys.append(key)
        return matching_keys

    def find_key_with_value_below(self, json_data, threshold):
        """
        딕셔너리에서 특정 값 이하를 가진 키들을 찾는 함수

        Args:
            json_data (dict): 딕셔너리 데이터
            threshold (int or float): 기준 값

        Returns:
            list: 기준 값 이하를 가진 키들
        """
        matching_keys = []

        for key, value in json_data.items():
            if isinstance(value, (int, float)) and value < threshold:
                matching_keys.append(key)
        return matching_keys

    def find_key_with_value_equal(self, json_data, threshold):
        """
        딕셔너리에서 특정 값과 같은 값을 가진 키들을 찾는 함수

        Args:
            json_data (dict): 딕셔너리 데이터
            threshold (Any): 기준 값
        
        Returns:
            list: 기준 값과 같은 값을 가진 키들
        """
        matching_keys = []

        for key, value in json_data.items():
            if isinstance(value, (int, float)) and value == threshold:
                matching_keys.append(key)
        return matching_keys    

    def text(self, lang, key):
        """
        언어 설정에 따라 텍스트를 반환하는 함수

        Args:
            lang (str): 언어 설정
            key (str): 텍스트 키
        """
        if lang in self.lang:
            lang_data = self.load_json(f"./language/{lang}.json")
            for k in lang_data:
                if k == key:
                    return lang_data[k]
                elif k != key:
                    pass
                else:
                    raise KeyError(f"Key '{key}' not found in language '{lang}'. Available keys: {list(lang_data.keys())}")
        else:
            raise ValueError(f"Language '{lang}' not supported. Available languages: {self.lang}")
                
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