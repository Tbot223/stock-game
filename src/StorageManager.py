#external modules
import os
import json
import time
import shutil

#internal modules
import AppCore


class StorageManager:
    """
    """
    def __init__(self):
        self.core = AppCore.AppCore()
        self.base_dir = "saves"
        self.backup_dir = "backup"
        os.makedirs(self.base_dir, exist_ok=True)

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
            return False, str(e), "StorageManager.load_data, R30-45"
        
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
            return False, str(e), "StorageManager.save_data, R47-68"
        
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
                self.save_metadata(save_id)
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
                        self.save_metadata(candidate)
                        self.core.save_json(user_data, user_path)
                        self.core.save_json(stocks_data, stocks_path)
                        #still developing
                        return True, None, None
                    i += 1
        except Exception as e:
            return False, str(e), "StorageManager.save_all, R70-106"
        
    def save_metadata(self, save_id):
        """
        저장 시간, 유저 이름, 플레이 시간 등 메타데이터 저장

        Args:
            save_id (str): 저장 ID (필수)
        """
        try:
            metadata = {
                "timestamp": time.strftime("%Y-%m-%d,%H:%M:%S", time.localtime()),
                "user_name": "example_user",  # self.menu.get_user_name()
                "play_time": 3600  # self.menu.get_play_time()
            }
            file_path = f"saves/{save_id}/metadata.json"
            self.core.save_json(metadata, file_path)
            return True, None, None
        except Exception as e:
            return False, str(e), "StorageManager.save_metadata, R108-125"
        
    def load_metadata(self, save_id):
        """
        저장된 메타데이터 불러오기

        Args:
            save_id (str): 불러올 저장 ID (필수)

        Returns:
            dict: 불러온 메타데이터
            실패 시 False, error 메시지, 컨텍스트 태그   
        """
        try:
            file_path = f"saves/{save_id}/metadata.json"
            return self.core.load_json(file_path)
        except Exception as e:
            return False, str(e), "StorageManager.load_metadata, R127-142"
        
    def list_saves(self):
        """
        saves/ 폴더 내의 모든 저장 ID를 반환

        Returns:
            list: 저장 ID 목록
        """
        try:
            saves = os.listdir(self.base_dir)
            return saves
        except Exception as e:
            return False, str(e), "StorageManager.list_saves, R145-160"
        
    def delete_save(self, save_id):
        """
        해당 저장 폴더를 삭제

        Args:
            save_id (str): 삭제할 저장 ID (필수)

        Returns:
            bool: 삭제 성공 여부
            실패 시 False, error 메시지, 컨텍스트 태그
        """
        try:
            save_path = os.path.join(self.base_dir, save_id)
            if os.path.exists(save_path):
                shutil.rmtree(save_path)
                return True, None, None
            else:
                return False, "Save ID does not exist.", "StorageManager.delete_save, R163-180"
        except Exception as e:
            return False, str(e), "StorageManager.delete_save, R162-182"
        
    def save_exists(self, save_id):
        """
        특정 저장 ID가 존재하는지 확인

        Args:
            save_id (str): 확인할 저장 ID (필수)

        Returns:
            bool: 존재 여부
        """
        save_path = os.path.join(self.base_dir, save_id)
        return os.path.exists(save_path) 
    
    def validate_save(self, save_id):
        """
        필수 파일(user.json, stocks.json 등) 존재 여부 확인

        Args:
            save_id (str): 확인할 저장 ID (필수)

        Returns:
            bool: 유효성 여부
            실패 시 False, error 메시지, 컨텍스트 태그
        """
        try:
            required_files = ["user.json", "stocks.json", "metadata.json"]
            save_path = os.path.join(self.base_dir, save_id)
            searched_file = os.listdir(save_path)
            missing_files = []
            for req_file in required_files:
                if req_file not in searched_file:
                    missing_files.append(req_file)
                else:
                    continue
            if missing_files != []:
                return False, f"Missing files: {', '.join(missing_files)}", "StorageManager.validate_save, R204-224"
            
            return True, None, None
        except Exception as e:
            return False, str(e), "StorageManager.validate_save, R204-224"
        
    def get_latest_save_id(self):
        """
        가장 최근에 생성된 저장 ID 반환

        Returns:
            str: 가장 최근 저장 ID
            실패 시 False, error 메시지, 컨텍스트 태그
        """
        try:
            saves = self.list_saves()
            if saves[0] is False:
                raise ValueError("Failed to list saves.")
            latest_save = None
            latest_time = 0
            for save in saves:
                    metadata = self.load_metadata(save)
                    if isinstance(metadata, tuple) and metadata[0] is False:
                        raise ValueError(f"Failed to load metadata for save: {save}")
                    timestamp_str = metadata.get("timestamp", "")
                    try:
                        timestamp = time.mktime(time.strptime(timestamp_str, "%Y-%m-%d,%H:%M:%S"))
                        if timestamp > latest_time:
                            latest_time = timestamp
                            latest_save = save
                    except ValueError:
                        continue
            if latest_save is None:
                return False, "No valid saves found.", "StorageManager.get_latest_save_id, R227-252"
            return latest_save
        except ValueError as e:
            return False, str(e), "StorageManager.get_latest_save_id, R226-254"
                
            
# StorageManager().save_all()
        
# print(StorageManager().validate_save("save_1"))

# print(StorageManager().get_latest_save_id())


        
        

"""
[StorageManager 업데이트 해야할 기능 목록]

    1. backup_save(save_id) - 현재 필요 없음, 나중에 필요하면 구현
    - 저장 시 backup/ 폴더에 복사본 생성
    - 데이터 손상 대비, 복구 기능과 연계 가능
    
"""