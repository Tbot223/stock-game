#external modules
import os
import json

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
            return False, str(e), "StorageManager.load_data, R15-23"
        
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
            if save_id is not None:
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
            user_data = {"example_key": "example_value"} # self.core.get_user_data()
            stocks_data = {"example_stock": 100} # self.core.get_stocks_data()

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
            return False, str(e), "StorageManager.save_all, R40-50"
        

storage_manager = StorageManager()
# Example usage:
# storage_manager.save_data({"example_key": "example_value"}, "user", "YESSSSS")
storage_manager.save_all()