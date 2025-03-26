#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
應用程序入口點 - AI 情境場域模型
"""

import os
import logging
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

# 導入自定義模塊
from psi_field import PsiFieldModel
from logic_core import LogicCore

# 配置日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 初始化 Flask 應用
app = Flask(__name__)

# 初始化模型
try:
    psi_field_model = PsiFieldModel()
    logic_core = LogicCore()
    logger.info("模型初始化成功")
except Exception as e:
    logger.error(f"模型初始化失敗: {str(e)}")
    raise

@app.route('/')
def index():
    """主頁面"""
    return render_template('index.html')

@app.route('/api/process', methods=['POST'])
def process_input():
    """處理用戶輸入並返回模型輸出"""
    try:
        data = request.json
        if not data or 'input' not in data:
            return jsonify({'error': '缺少輸入數據'}), 400
        
        input_text = data['input']
        context = data.get('context', {})
        
        # 使用 psi_field 模型處理輸入
        psi_result = psi_field_model.process(input_text, context)
        
        # 使用 logic_core 進行邏輯推理
        result = logic_core.analyze(psi_result)
        
        return jsonify({
            'status': 'success',
            'result': result,
            'psi_field_data': psi_result.to_dict() if hasattr(psi_result, 'to_dict') else psi_result
        })
    except Exception as e:
        logger.error(f"處理請求時發生錯誤: {str(e)}")
        return jsonify({'error': f'處理請求時發生錯誤: {str(e)}'}), 500

@app.route('/api/model/status', methods=['GET'])
def model_status():
    """返回模型狀態信息"""
    try:
        psi_status = psi_field_model.get_status()
        logic_status = logic_core.get_status()
        
        return jsonify({
            'status': 'online',
            'psi_field': psi_status,
            'logic_core': logic_status,
            'version': os.environ.get('MODEL_VERSION', '1.0.0')
        })
    except Exception as e:
        logger.error(f"獲取模型狀態時發生錯誤: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/train', methods=['POST'])
def train_model():
    """訓練或微調模型"""
    try:
        data = request.json
        if not data or 'training_data' not in data:
            return jsonify({'error': '缺少訓練數據'}), 400
        
        training_data = data['training_data']
        epochs = data.get('epochs', 1)
        learning_rate = data.get('learning_rate', 0.001)
        
        # 訓練 psi_field 模型
        training_result = psi_field_model.train(
            training_data, 
            epochs=epochs, 
            learning_rate=learning_rate
        )
        
        return jsonify({
            'status': 'success',
            'message': '模型訓練完成',
            'metrics': training_result
        })
    except Exception as e:
        logger.error(f"訓練模型時發生錯誤: {str(e)}")
        return jsonify({'error': f'訓練模型時發生錯誤: {str(e)}'}), 500

@app.route('/api/evaluate', methods=['POST'])
def evaluate_model():
    """評估模型表現"""
    try:
        data = request.json
        if not data or 'evaluation_data' not in data:
            return jsonify({'error': '缺少評估數據'}), 400
        
        evaluation_data = data['evaluation_data']
        
        # 評估 psi_field 模型
        psi_metrics = psi_field_model.evaluate(evaluation_data)
        
        # 評估 logic_core
        logic_metrics = logic_core.evaluate(evaluation_data)
        
        return jsonify({
            'status': 'success',
            'psi_field_metrics': psi_metrics,
            'logic_core_metrics': logic_metrics
        })
    except Exception as e:
        logger.error(f"評估模型時發生錯誤: {str(e)}")
        return jsonify({'error': f'評估模型時發生錯誤: {str(e)}'}), 500

@app.route('/api/visualize', methods=['POST'])
def visualize_field():
    """視覺化情境場域"""
    try:
        data = request.json
        if not data or 'input' not in data:
            return jsonify({'error': '缺少輸入數據'}), 400
        
        input_text = data['input']
        
        # 生成視覺化數據
        visualization = psi_field_model.visualize(input_text)
        
        return jsonify({
            'status': 'success',
            'visualization_data': visualization
        })
    except Exception as e:
        logger.error(f"生成視覺化時發生錯誤: {str(e)}")
        return jsonify({'error': f'生成視覺化時發生錯誤: {str(e)}'}), 500

@app.errorhandler(404)
def not_found(error):
    """處理 404 錯誤"""
    return jsonify({'error': '請求的資源不存在'}), 404

@app.errorhandler(500)
def server_error(error):
    """處理 500 錯誤"""
    logger.error(f"服務器錯誤: {str(error)}")
    return jsonify({'error': '服務器內部錯誤'}), 500

if __name__ == '__main__':
    # 從環境變數獲取端口，默認為 5000
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    logger.info(f"應用啟動於端口 {port}，調試模式: {debug}")
    app.run(host='0.0.0.0', port=port, debug=debug)
