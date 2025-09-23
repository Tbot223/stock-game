#external modules
import os
import json
import time

#internal modules
import AppCore


class StorageManager:
    """
    """
    def __init__(self):
        self.core = AppCore.AppCore()
        self.base_dir = "saves"
        os.makedirs(self.base_dir, exist_ok=True)

    def _generate_save_id(self):
        """
        saves/save_1, save_2, ... 중 존재하지 않는 가장 낮은 번호를 찾아 반환
        """
        i = 1
        while True:
            candidate = f"save_{i}"
            candidate_path = os.path.join(self.base_dir, candidate)
            if not os.path.exists(candidate_path):
                return candidate
            i += 1

    def load_data(self, save_type, save_id="latest"):
        """
        /saves/(save_id)/(save_type).json 에서 데이터를 불러옵니다.

        Args:
            save_type (str): 불러올 데이터 유형 (stocks, user)
            save_id (str): 불러올 저장 ID (선택적, 기본값 "latest")
        Returns:
            dict: 불러온 데이터
            실패 시 False, error 메시지, 컨텍스트 태그   
        """
        try:
            file_path = f"saves/{save_id}/{save_type}.json"
            return self.core.load_json(file_path)
        except Exception as e:
            return False, str(e), "StorageManager.load_data, R29-44"
        
    def save_data(self, save_data, save_type, save_id):
        """
        /saves/(save_id)/(save_type).json 에 데이터를 저장합니다.

        Args:
            save_data (dict): 저장할 데이터
            save_type (str): 저장 유형 (stocks, user)
            save_id (str): 저장 ID (필수, 미리 생성한 세이브 파일에만 사용할 것, 세이브 생성은 save_all 사용)

        Returns:
            bool: 저장 성공 여부
            실패 시 False, error 메시지, 컨텍스트 태그
        """
        try:
            if save_id is None:
                return False, "save_id cannot be None. Use save_all to create a new save.", "StorageManager.save_data, R48-64"
            file_path = f"saves/{save_id}/{save_type}.json"
            self.core.save_json(save_data, file_path)
            return True, None, None

        except Exception as e:
            return False, str(e), "StorageManager.save_data, R25-33"
        
    def save_all(self, save_id=None):
        """
        user, stocks 데이터를 모두 저장합니다.

        Args:
            save_id (str): 저장 ID (선택적, 기본값 None - 새로운 ID 생성)

        Returns:
            bool: 저장 성공 여부
            실패 시 False, error 메시지, 컨텍스트 태그
        """
        try:
            user_data = {"example_key": "example_value"} #ss self.menu.get_user_data()
            stocks_data = {"example_stock": 100} # self.menu.get_stocks_data()

            if save_id is not None:
                file_path_user = f"saves/{save_id}/user.json"
                file_path_stocks = f"saves/{save_id}/stocks.json"
                self.core.save_json(user_data, file_path_user)
                self.core.save_json(stocks_data, file_path_stocks)
                return True, None, None
            else:
                i = 1
                while True:
                    candidate = f"save_{i}"
                    candidate_path = os.path.join(self.base_dir, candidate)
                    if not os.path.exists(candidate_path):
                        os.makedirs(candidate_path, exist_ok=True)
                        user_path = f"saves/{candidate}/user.json"
                        stocks_path = f"saves/{candidate}/stocks.json"
                        self.core.save_json(user_data, user_path)
                        self.core.save_json(stocks_data, stocks_path)
                        #still developing
                        return True, None, None
                    i += 1
        except Exception as e:
            return False, str(e), "StorageManager.save_all, R69-105"
        
    def save_metadata(self, save_id):
        """
        저장 시간, 유저 이름, 플레이 시간 등 메타데이터 저장

        Args:
            save_id (str): 저장 ID (필수)
        """
        try:
            metadata = {
                "timestamp": time.time(),
                "user_name": "example_user",  # self.menu.get_user_name()
                "play_time": 3600  # self.menu.get_play_time()
            }
            file_path = f"saves/{save_id}/metadata.json"
            self.core.save_json(metadata, file_path)
            return True, None, None
        except Exception as e:
            return False, str(e), "StorageManager.save_metadata, R109-123"
        
        

"""
[StorageManager 업데이트 해야할 기능 목록]

    1. save_metadata(save_id)
    - 저장 시간, 유저 이름, 플레이 시간 등 메타데이터 저장
    - 세이브 슬롯에 정보 표시 가능, UX 향상

    2. load_metadata(save_id)
    - 저장된 메타데이터 불러오기
    - UI에 세이브 정보 표시 가능

    3. list_saves()
    - saves/ 폴더 내의 모든 세이브 ID를 반환
    - 유저가 저장 슬롯을 선택하거나 UI에 표시 가능

    4. delete_save(save_id)
    - 해당 세이브 폴더를 삭제
    - 오래된 세이브 정리, UI에서 “삭제” 버튼 구현 가능

    5. save_exists(save_id)
    - 특정 세이브 ID가 존재하는지 확인
    - 덮어쓰기 여부 판단, 경고 메시지 출력에 활용

    6. backup_save(save_id)
    - 저장 시 backup/ 폴더에 복사본 생성
    - 데이터 손상 대비, 복구 기능과 연계 가능

    7. validate_save(save_id)
    - 필수 파일(user.json, stocks.json 등) 존재 여부 확인
    - 불완전한 세이브 방지, 로딩 안정성 향상

    8. get_latest_save_id()
        - 가장 최근에 생성된 세이브 ID 반환
        - 기본 로딩 슬롯 지정에 활용
"""