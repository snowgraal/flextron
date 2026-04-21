from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import requests
from datetime import datetime
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

app = Flask(__name__)

# ===== НАСТРОЙКИ EMAIL =====
# ВНИМАНИЕ: Пароль нужно сменить! Используйте новый пароль
SMTP_SERVER = "smtp.mail.ru"
SMTP_PORT = 465
EMAIL_LOGIN = "snowgraal@mail.ru"
EMAIL_PASSWORD = "AKGLVIObCQBt4mGSHdca"  # ЗАМЕНИТЕ НА НОВЫЙ ПАРОЛЬ!
EMAIL_TO = "snowgraal@mail.ru"  # сюда будут приходить заявки
# =================================

# ==================== ПОЛНЫЕ ДАННЫЕ ПРАЙС-ЛИСТА ====================

PRODUCTS = {
    # ========== ТРУБЫ НПВХ НАРУЖНЫЕ (РЫЖИЕ) ==========
    'pipes_npvh_outdoor_sn2': {
        'title': 'Трубы НПВХ наружные (рыжие) SN2 (2,0 мм)',
        'icon': 'fa-pipe-valve',
        'color': '#ff6b00',
        'image': 'pipe-red-110mm.jpg',
        'product_list': [
            {'name': 'Труба НПВХ 110 мм наружная SN2', 'spec': '2,0 мм', 'length': '0,25 м', 'pack': '10 шт'},
            {'name': 'Труба НПВХ 110 мм наружная SN2', 'spec': '2,0 мм', 'length': '0,5 м', 'pack': '10 шт'},
            {'name': 'Труба НПВХ 110 мм наружная SN2', 'spec': '2,0 мм', 'length': '1 м', 'pack': '6 шт'},
            {'name': 'Труба НПВХ 110 мм наружная SN2', 'spec': '2,0 мм', 'length': '1,5 м', 'pack': '6 шт'},
            {'name': 'Труба НПВХ 110 мм наружная SN2', 'spec': '2,0 мм', 'length': '2 м', 'pack': '6 шт'},
            {'name': 'Труба НПВХ 110 мм наружная SN2', 'spec': '2,0 мм', 'length': '3 м', 'pack': '6 шт'},
            {'name': 'Труба НПВХ 110 мм наружная SN2', 'spec': '2,0 мм', 'length': '4 м', 'pack': '6 шт'},
            {'name': 'Труба НПВХ 110 мм наружная SN2', 'spec': '2,0 мм', 'length': '5 м', 'pack': '6 шт'},
            {'name': 'Труба НПВХ 110 мм наружная SN2', 'spec': '2,0 мм', 'length': '6 м', 'pack': '6 шт'},
        ]
    },
    'pipes_npvh_outdoor_sn4': {
        'title': 'Трубы НПВХ наружные (рыжие) SN4 (2,5 мм)',
        'icon': 'fa-pipe-valve',
        'color': '#ff6b00',
        'image': 'pipe-red-110mm.jpg',
        'product_list': [
            {'name': 'Труба НПВХ 110 мм наружная SN4', 'spec': '2,5 мм', 'length': '0,5 м', 'pack': '6 шт'},
            {'name': 'Труба НПВХ 110 мм наружная SN4', 'spec': '2,5 мм', 'length': '1 м', 'pack': '6 шт'},
            {'name': 'Труба НПВХ 110 мм наружная SN4', 'spec': '2,5 мм', 'length': '1,5 м', 'pack': '6 шт'},
            {'name': 'Труба НПВХ 110 мм наружная SN4', 'spec': '2,5 мм', 'length': '2 м', 'pack': '6 шт'},
            {'name': 'Труба НПВХ 110 мм наружная SN4', 'spec': '2,5 мм', 'length': '3 м', 'pack': '6 шт'},
            {'name': 'Труба НПВХ 110 мм наружная SN4', 'spec': '2,5 мм', 'length': '4 м', 'pack': '6 шт'},
            {'name': 'Труба НПВХ 110 мм наружная SN4', 'spec': '2,5 мм', 'length': '5 м', 'pack': '6 шт'},
            {'name': 'Труба НПВХ 110 мм наружная SN4', 'spec': '2,5 мм', 'length': '6 м', 'pack': '6 шт'},
        ]
    },
    'pipes_npvh_outdoor_sn8': {
        'title': 'Трубы НПВХ наружные (рыжие) SN8 (3,2 мм)',
        'icon': 'fa-pipe-valve',
        'color': '#ff6b00',
        'image': 'pipe-red-110mm.jpg',
        'product_list': [
            {'name': 'Труба НПВХ 110 мм наружная SN8', 'spec': '3,2 мм', 'length': '0,25 м', 'pack': '10 шт'},
            {'name': 'Труба НПВХ 110 мм наружная SN8', 'spec': '3,2 мм', 'length': '0,5 м', 'pack': '6 шт'},
            {'name': 'Труба НПВХ 110 мм наружная SN8', 'spec': '3,2 мм', 'length': '1 м', 'pack': '6 шт'},
            {'name': 'Труба НПВХ 110 мм наружная SN8', 'spec': '3,2 мм', 'length': '1,5 м', 'pack': '6 шт'},
        ]
    },
    'pipes_npvh_outdoor_160': {
        'title': 'Трубы НПВХ наружные 160 мм (3,2 мм)',
        'icon': 'fa-pipe-valve',
        'color': '#ff6b00',
        'image': 'pipe-red-110mm.jpg',
        'product_list': [
            {'name': 'Труба НПВХ 160 мм наружная', 'spec': '3,2 мм', 'length': '0,5 м', 'pack': '4 шт'},
            {'name': 'Труба НПВХ 160 мм наружная', 'spec': '3,2 мм', 'length': '1 м', 'pack': '4 шт'},
            {'name': 'Труба НПВХ 160 мм наружная', 'spec': '3,2 мм', 'length': '1,5 м', 'pack': '4 шт'},
            {'name': 'Труба НПВХ 160 мм наружная', 'spec': '3,2 мм', 'length': '2 м', 'pack': '4 шт'},
            {'name': 'Труба НПВХ 160 мм наружная', 'spec': '3,2 мм', 'length': '3 м', 'pack': '4 шт'},
            {'name': 'Труба НПВХ 160 мм наружная', 'spec': '3,2 мм', 'length': '4 м', 'pack': '4 шт'},
            {'name': 'Труба НПВХ 160 мм наружная', 'spec': '3,2 мм', 'length': '5 м', 'pack': '4 шт'},
            {'name': 'Труба НПВХ 160 мм наружная', 'spec': '3,2 мм', 'length': '6 м', 'pack': '4 шт'},
        ]
    },

    # ========== ТРУБЫ НПВХ ВНУТРЕННИЕ (СЕРЫЕ) ==========
    'pipes_npvh_indoor': {
        'title': 'Трубы НПВХ внутренние (серые) 2,0 мм',
        'icon': 'fa-pipe-valve',
        'color': '#6c757d',
        'image': 'pipe-gray-110mm.jpg',
        'product_list': [
            {'name': 'Труба НПВХ 110 мм серая', 'spec': '2,0 мм', 'length': '0,25 м', 'pack': '10 шт'},
            {'name': 'Труба НПВХ 110 мм серая', 'spec': '2,0 мм', 'length': '0,5 м', 'pack': '6 шт'},
            {'name': 'Труба НПВХ 110 мм серая', 'spec': '2,0 мм', 'length': '1 м', 'pack': '6 шт'},
            {'name': 'Труба НПВХ 110 мм серая', 'spec': '2,0 мм', 'length': '1,5 м', 'pack': '6 шт'},
            {'name': 'Труба НПВХ 110 мм серая', 'spec': '2,0 мм', 'length': '2 м', 'pack': '6 шт'},
            {'name': 'Труба НПВХ 110 мм серая', 'spec': '2,0 мм', 'length': '3 м', 'pack': '6 шт'},
            {'name': 'Труба НПВХ 110 мм серая', 'spec': '2,0 мм', 'length': '4 м', 'pack': '6 шт'},
            {'name': 'Труба НПВХ 110 мм серая', 'spec': '2,0 мм', 'length': '5 м', 'pack': '6 шт'},
            {'name': 'Труба НПВХ 110 мм серая', 'spec': '2,0 мм', 'length': '6 м', 'pack': '6 шт'},
        ]
    },

    # ========== ТРУБЫ ПП СЕРЫЕ (внутренняя канализация) ==========
    'pipes_pp_gray': {
        'title': 'Трубы ПП серые (для внутренней канализации)',
        'icon': 'fa-pipe-valve',
        'color': '#6c757d',
        'image': 'pipe-pp-gray.jpg',
        'product_list': [
            {'name': 'Труба ПП 32 мм серая', 'spec': '1,8 мм', 'length': '0,25 м', 'pack': '50 шт'},
            {'name': 'Труба ПП 32 мм серая', 'spec': '1,8 мм', 'length': '0,5 м', 'pack': '50 шт'},
            {'name': 'Труба ПП 32 мм серая', 'spec': '1,8 мм', 'length': '1 м', 'pack': '50 шт'},
            {'name': 'Труба ПП 32 мм серая', 'spec': '1,8 мм', 'length': '1,8 м', 'pack': '10 шт'},
            {'name': 'Труба ПП 32 мм серая', 'spec': '1,8 мм', 'length': '2 м', 'pack': '50 шт'},
            {'name': 'Труба ПП 32 мм серая', 'spec': '1,8 мм', 'length': '3 м', 'pack': '10 шт'},
            {'name': 'Труба ПП 40 мм серая', 'spec': '1,8 мм', 'length': '0,25 м', 'pack': '50 шт'},
            {'name': 'Труба ПП 40 мм серая', 'spec': '1,8 мм', 'length': '0,5 м', 'pack': '50 шт'},
            {'name': 'Труба ПП 40 мм серая', 'spec': '1,8 мм', 'length': '1 м', 'pack': '50 шт'},
            {'name': 'Труба ПП 40 мм серая', 'spec': '1,8 мм', 'length': '1,8 м', 'pack': '10 шт'},
            {'name': 'Труба ПП 40 мм серая', 'spec': '1,8 мм', 'length': '2 м', 'pack': '10 шт'},
            {'name': 'Труба ПП 40 мм серая', 'spec': '1,8 мм', 'length': '3 м', 'pack': '10 шт'},
            {'name': 'Труба ПП 50 мм серая', 'spec': '1,8 мм', 'length': '0,25 м', 'pack': '40 шт'},
            {'name': 'Труба ПП 50 мм серая', 'spec': '1,8 мм', 'length': '0,5 м', 'pack': '35 шт'},
            {'name': 'Труба ПП 50 мм серая', 'spec': '1,8 мм', 'length': '1 м', 'pack': '40 шт'},
            {'name': 'Труба ПП 50 мм серая', 'spec': '1,8 мм', 'length': '1,5 м', 'pack': '40 шт'},
            {'name': 'Труба ПП 50 мм серая', 'spec': '1,8 мм', 'length': '2 м', 'pack': '30 шт'},
            {'name': 'Труба ПП 50 мм серая', 'spec': '1,8 мм', 'length': '3 м', 'pack': '30 шт'},
            {'name': 'Труба ПП 75 мм серая', 'spec': '2,0 мм', 'length': '0,25 м', 'pack': '20 шт'},
            {'name': 'Труба ПП 75 мм серая', 'spec': '2,0 мм', 'length': '0,5 м', 'pack': '20 шт'},
            {'name': 'Труба ПП 75 мм серая', 'spec': '2,0 мм', 'length': '1 м', 'pack': '20 шт'},
            {'name': 'Труба ПП 75 мм серая', 'spec': '2,0 мм', 'length': '2 м', 'pack': '10 шт'},
            {'name': 'Труба ПП 75 мм серая', 'spec': '2,0 мм', 'length': '3 м', 'pack': '10 шт'},
            {'name': 'Труба ПП 110 мм серая', 'spec': '2,2 мм', 'length': '0,25 м', 'pack': '10 шт'},
            {'name': 'Труба ПП 110 мм серая', 'spec': '2,2 мм', 'length': '0,5 м', 'pack': '10 шт'},
            {'name': 'Труба ПП 110 мм серая', 'spec': '2,2 мм', 'length': '1 м', 'pack': '10 шт'},
            {'name': 'Труба ПП 110 мм серая', 'spec': '2,2 мм', 'length': '1,5 м', 'pack': '10 шт'},
            {'name': 'Труба ПП 110 мм серая', 'spec': '2,2 мм', 'length': '2 м', 'pack': '10 шт'},
            {'name': 'Труба ПП 110 мм серая', 'spec': '2,2 мм', 'length': '3 м', 'pack': '10 шт'},
            {'name': 'Труба ПП 110 мм серая', 'spec': '2,2 мм', 'length': '4 м', 'pack': '10 шт'},
            {'name': 'Труба ПП PPR 110 мм', 'spec': '2,7 мм', 'length': '0,25 м', 'pack': '10 шт'},
            {'name': 'Труба ПП PPR 110 мм', 'spec': '2,7 мм', 'length': '0,5 м', 'pack': '10 шт'},
            {'name': 'Труба ПП PPR 110 мм', 'spec': '2,7 мм', 'length': '1 м', 'pack': '10 шт'},
            {'name': 'Труба ПП PPR 110 мм', 'spec': '2,7 мм', 'length': '2 м', 'pack': '10 шт'},
            {'name': 'Труба ПП PPR 110 мм', 'spec': '2,7 мм', 'length': '3 м', 'pack': '10 шт'},
            {'name': 'Труба ПП PPR 110 мм', 'spec': '2,7 мм', 'length': '4 м', 'pack': '10 шт'},
        ]
    },

    # ========== ТРУБЫ ПП РЫЖИЕ (наружная канализация) ==========
    'pipes_pp_red': {
        'title': 'Трубы ПП рыжие (для наружной канализации)',
        'icon': 'fa-pipe-valve',
        'color': '#ff6b00',
        'image': 'pipe-pp-red.jpg',
        'product_list': [
            {'name': 'Труба ПП 110 мм SN2 рыжая', 'spec': 'SN2', 'length': '0,5 м', 'pack': '10 шт'},
            {'name': 'Труба ПП 110 мм SN2 рыжая', 'spec': 'SN2', 'length': '1 м', 'pack': '10 шт'},
            {'name': 'Труба ПП 110 мм SN2 рыжая', 'spec': 'SN2', 'length': '1,5 м', 'pack': '10 шт'},
            {'name': 'Труба ПП 110 мм SN2 рыжая', 'spec': 'SN2', 'length': '2 м', 'pack': '10 шт'},
            {'name': 'Труба ПП 110 мм SN2 рыжая', 'spec': 'SN2', 'length': '3 м', 'pack': '10 шт'},
            {'name': 'Труба ПП 110 мм SN2 рыжая', 'spec': 'SN2', 'length': '4 м', 'pack': '10 шт'},
            {'name': 'Труба ПП 110 мм рыжая 3,2 мм', 'spec': '3,2 мм', 'length': '0,5 м', 'pack': '10 шт'},
            {'name': 'Труба ПП 110 мм рыжая 3,2 мм', 'spec': '3,2 мм', 'length': '1 м', 'pack': '10 шт'},
            {'name': 'Труба ПП 110 мм рыжая 3,2 мм', 'spec': '3,2 мм', 'length': '1,5 м', 'pack': '10 шт'},
            {'name': 'Труба ПП 110 мм рыжая 3,2 мм', 'spec': '3,2 мм', 'length': '2 м', 'pack': '10 шт'},
            {'name': 'Труба ПП 110 мм рыжая 3,2 мм', 'spec': '3,2 мм', 'length': '3 м', 'pack': '10 шт'},
            {'name': 'Труба ПП 110 мм рыжая 3,2 мм', 'spec': '3,2 мм', 'length': '4 м', 'pack': '10 шт'},
            {'name': 'Труба ПП 160 мм рыжая', 'spec': '3,8 мм', 'length': '0,5 м', 'pack': '10 шт'},
            {'name': 'Труба ПП 160 мм рыжая', 'spec': '3,8 мм', 'length': '1 м', 'pack': '10 шт'},
            {'name': 'Труба ПП 160 мм рыжая', 'spec': '3,8 мм', 'length': '2 м', 'pack': '10 шт'},
            {'name': 'Труба ПП 160 мм рыжая', 'spec': '3,8 мм', 'length': '3 м', 'pack': '10 шт'},
            {'name': 'Труба ПП 160 мм рыжая', 'spec': '3,8 мм', 'length': '4 м', 'pack': '10 шт'},
            {'name': 'Труба ПП 200 мм рыжая', 'spec': '5,2 мм', 'length': '0,5 м', 'pack': '2 шт'},
            {'name': 'Труба ПП 200 мм рыжая', 'spec': '5,2 мм', 'length': '1 м', 'pack': '2 шт'},
            {'name': 'Труба ПП 200 мм рыжая', 'spec': '5,2 мм', 'length': '2 м', 'pack': '2 шт'},
            {'name': 'Труба ПП 200 мм рыжая', 'spec': '5,2 мм', 'length': '3 м', 'pack': '2 шт'},
            {'name': 'Труба ПП 200 мм рыжая', 'spec': '5,2 мм', 'length': '4 м', 'pack': '2 шт'},
        ]
    },

    # ========== ФИТИНГИ ПП ==========
    'fittings_elbows_50': {
        'title': 'Отводы ПП 50 мм',
        'icon': 'fa-share-alt',
        'color': '#ff6b00',
        'image': 'fitting-elbow.jpg',
        'product_list': [
            {'name': 'Отвод ПП 50 мм', 'spec': '15°', 'pack': '100 шт'},
            {'name': 'Отвод ПП 50 мм', 'spec': '22°', 'pack': '100 шт'},
            {'name': 'Отвод ПП 50 мм', 'spec': '30°', 'pack': '100 шт'},
            {'name': 'Отвод ПП 50 мм', 'spec': '45°', 'pack': '100 шт'},
            {'name': 'Отвод ПП 50 мм', 'spec': '67°', 'pack': '100 шт'},
            {'name': 'Отвод ПП 50 мм', 'spec': '90°', 'pack': '100 шт'},
        ]
    },
    'fittings_elbows_110': {
        'title': 'Отводы ПП 110 мм',
        'icon': 'fa-share-alt',
        'color': '#ff6b00',
        'image': 'fitting-elbow-110.jpg',
        'product_list': [
            {'name': 'Отвод ПП 110 мм', 'spec': '15°', 'pack': '20 шт'},
            {'name': 'Отвод ПП 110 мм', 'spec': '30°', 'pack': '20 шт'},
            {'name': 'Отвод ПП 110 мм', 'spec': '45°', 'pack': '20 шт'},
            {'name': 'Отвод ПП 110 мм', 'spec': '67°', 'pack': '15 шт'},
            {'name': 'Отвод ПП 110 мм', 'spec': '90°', 'pack': '15 шт'},
        ]
    },
    'fittings_tees': {
        'title': 'Тройники ПП 110 мм',
        'icon': 'fa-code-branch',
        'color': '#ff6b00',
        'image': 'fitting-tee.jpg',
        'product_list': [
            {'name': 'Тройник ПП 110/110/45°', 'spec': '110/110/45°', 'pack': '7 шт'},
            {'name': 'Тройник ПП 110/110/90°', 'spec': '110/110/90°', 'pack': '10 шт'},
            {'name': 'Тройник ПП 110/50/45°', 'spec': '110/50/45°', 'pack': '15 шт'},
            {'name': 'Тройник ПП 110/50/90°', 'spec': '110/50/90°', 'pack': '15 шт'},
        ]
    },
    'fittings_tees_small': {
        'title': 'Тройники ПП малые (32, 40, 50 мм)',
        'icon': 'fa-code-branch',
        'color': '#ff6b00',
        'image': 'fitting-tee-small.jpg',
        'product_list': [
            {'name': 'Тройник ПП 32/32/45°', 'spec': '32/32/45°', 'pack': '80 шт'},
            {'name': 'Тройник ПП 32/32/90°', 'spec': '32/32/90°', 'pack': '80 шт'},
            {'name': 'Тройник ПП 40/40/45°', 'spec': '40/40/45°', 'pack': '40 шт'},
            {'name': 'Тройник ПП 40/40/90°', 'spec': '40/40/90°', 'pack': '40 шт'},
            {'name': 'Тройник ПП 50/50/45°', 'spec': '50/50/45°', 'pack': '50 шт'},
            {'name': 'Тройник ПП 50/50/90°', 'spec': '50/50/90°', 'pack': '50 шт'},
        ]
    },
    'fittings_crosses': {
        'title': 'Крестовины ПП 110 мм',
        'icon': 'fa-plus-square',
        'color': '#ff6b00',
        'image': 'fitting-cross.jpg',
        'product_list': [
            {'name': 'Крестовина ПП 110/110/110/45°', 'spec': '110/110/110/45°', 'pack': '6 шт'},
            {'name': 'Крестовина ПП 110/110/110/90°', 'spec': '110/110/110/90°', 'pack': '8 шт'},
            {'name': 'Крестовина ПП 110/110/50/90°', 'spec': '110/110/50/90°', 'pack': '8 шт'},
            {'name': 'Крестовина ПП 110/50/50/45°', 'spec': '110/50/50/45°', 'pack': '15 шт'},
            {'name': 'Крестовина ПП 110/50/50/90°', 'spec': '110/50/50/90°', 'pack': '15 шт'},
        ]
    },
    'fittings_crosses_small': {
        'title': 'Крестовины ПП 50 мм',
        'icon': 'fa-plus-square',
        'color': '#ff6b00',
        'image': 'fitting-cross-small.jpg',
        'product_list': [
            {'name': 'Крестовина ПП 50/50/50/45°', 'spec': '50/50/50/45°', 'pack': '40 шт'},
            {'name': 'Крестовина ПП 50/50/50/90°', 'spec': '50/50/50/90°', 'pack': '40 шт'},
        ]
    },
    'fittings_crosses_2plane': {
        'title': 'Крестовины ПП двухплоскостные',
        'icon': 'fa-plus-square',
        'color': '#ff6b00',
        'image': 'fitting-cross-2plane.jpg',
        'product_list': [
            {'name': 'Крестовина двухплоскостная 110/110/110/90°', 'spec': '2-плоскостная', 'pack': '8 шт'},
            {'name': 'Крестовина двухплоскостная 110/50/50/90°', 'spec': '2-плоскостная', 'pack': '10 шт'},
        ]
    },
    'fittings_couplings': {
        'title': 'Муфты ПП 110 мм',
        'icon': 'fa-link',
        'color': '#ff6b00',
        'image': 'fitting-coupling.jpg',
        'product_list': [
            {'name': 'Муфта ПП 110 мм', 'spec': '110 мм', 'pack': '25 шт'},
        ]
    },
    'fittings_couplings_small': {
        'title': 'Муфты ПП малые (32, 40, 50 мм)',
        'icon': 'fa-link',
        'color': '#ff6b00',
        'image': 'fitting-coupling-small.jpg',
        'product_list': [
            {'name': 'Муфта ПП 32 мм', 'spec': '32 мм', 'pack': '300 шт'},
            {'name': 'Муфта ПП 40 мм', 'spec': '40 мм', 'pack': '80 шт'},
            {'name': 'Муфта ПП 50 мм', 'spec': '50 мм', 'pack': '100 шт'},
        ]
    },
    'fittings_couplings_outdoor': {
        'title': 'Муфты ПП наружные',
        'icon': 'fa-link',
        'color': '#ff6b00',
        'image': 'fitting-coupling-outdoor.jpg',
        'product_list': [
            {'name': 'Муфта наружная 110 мм', 'spec': 'наружная 110 мм', 'pack': '25 шт'},
        ]
    },
    'fittings_caps': {
        'title': 'Заглушки ПП 110 мм',
        'icon': 'fa-stop-circle',
        'color': '#ff6b00',
        'image': 'fitting-cap.jpg',
        'product_list': [
            {'name': 'Заглушка ПП 110 мм', 'spec': '110 мм', 'pack': '100 шт'},
        ]
    },
    'fittings_caps_small': {
        'title': 'Заглушки ПП малые (32, 40, 50 мм)',
        'icon': 'fa-stop-circle',
        'color': '#ff6b00',
        'image': 'fitting-cap-small.jpg',
        'product_list': [
            {'name': 'Заглушка ПП 32 мм', 'spec': '32 мм', 'pack': '300 шт'},
            {'name': 'Заглушка ПП 40 мм', 'spec': '40 мм', 'pack': '200 шт'},
            {'name': 'Заглушка ПП 50 мм', 'spec': '50 мм', 'pack': '500 шт'},
        ]
    },
    'fittings_caps_outdoor': {
        'title': 'Заглушки ПП наружные',
        'icon': 'fa-stop-circle',
        'color': '#ff6b00',
        'image': 'fitting-cap-outdoor.jpg',
        'product_list': [
            {'name': 'Заглушка наружная 110 мм', 'spec': 'наружная 110 мм', 'pack': '100 шт'},
        ]
    },
    'fittings_compensators': {
        'title': 'Компенсаторы ПП',
        'icon': 'fa-sync-alt',
        'color': '#ff6b00',
        'image': 'fitting-compensator.jpg',
        'product_list': [
            {'name': 'Компенсатор ПП 110 мм', 'spec': '110 мм', 'pack': '12 шт'},
            {'name': 'Компенсатор ПП 50 мм', 'spec': '50 мм', 'pack': '50 шт'},
        ]
    },
    'fittings_compensators_outdoor': {
        'title': 'Компенсаторы ПП наружные',
        'icon': 'fa-sync-alt',
        'color': '#ff6b00',
        'image': 'fitting-compensator-outdoor.jpg',
        'product_list': [
            {'name': 'Компенсатор наружный 110 мм', 'spec': 'наружный 110 мм', 'pack': '12 шт'},
        ]
    },
    'fittings_revisions': {
        'title': 'Ревизии ПП',
        'icon': 'fa-search',
        'color': '#ff6b00',
        'image': 'fitting-revision.jpg',
        'product_list': [
            {'name': 'Ревизия ПП 110 мм', 'spec': '110 мм', 'pack': '10 шт'},
            {'name': 'Ревизия ПП 50 мм', 'spec': '50 мм', 'pack': '100 шт'},
        ]
    },
    'fittings_revisions_outdoor': {
        'title': 'Ревизии ПП наружные',
        'icon': 'fa-search',
        'color': '#ff6b00',
        'image': 'fitting-revision-outdoor.jpg',
        'product_list': [
            {'name': 'Ревизия наружная 110 мм', 'spec': 'наружная 110 мм', 'pack': '10 шт'},
        ]
    },
    'fittings_aerators': {
        'title': 'Аэраторы ПП',
        'icon': 'fa-fan',
        'color': '#ff6b00',
        'image': 'fitting-aerator.jpg',
        'product_list': [
            {'name': 'Аэратор ПП 110 мм', 'spec': '110 мм', 'pack': '33 шт'},
            {'name': 'Аэратор ПП 50 мм', 'spec': '50 мм', 'pack': '100 шт'},
        ]
    },
    'fittings_umbrellas': {
        'title': 'Зонты ПП 110 мм',
        'icon': 'fa-umbrella',
        'color': '#ff6b00',
        'image': 'fitting-umbrella.jpg',
        'product_list': [
            {'name': 'Зонт ПП 110 мм разборный', 'spec': 'разборный', 'pack': '6 шт'},
            {'name': 'Зонт ПП 110 мм цельнолитой', 'spec': 'цельнолитой', 'pack': '50 шт'},
        ]
    },
    'fittings_umbrellas_outdoor': {
        'title': 'Зонты ПП наружные',
        'icon': 'fa-umbrella',
        'color': '#ff6b00',
        'image': 'fitting-umbrella-outdoor.jpg',
        'product_list': [
            {'name': 'Зонт ПП 110 мм наружный', 'spec': 'наружный', 'pack': '50 шт'},
            {'name': 'Зонт ПП 160 мм наружный', 'spec': 'наружный', 'pack': '24 шт'},
        ]
    },
    'fittings_traps': {
        'title': 'Трапы прямые ПП',
        'icon': 'fa-water',
        'color': '#ff6b00',
        'image': 'fitting-trap.jpg',
        'product_list': [
            {'name': 'Трап прямой ПП 110 мм', 'spec': 'прямой', 'pack': '10 шт'},
            {'name': 'Трап прямой ПП 50 мм 10/10', 'spec': 'прямой 10/10', 'pack': '25 шт'},
            {'name': 'Трап прямой ПП 50 мм 15/15', 'spec': 'прямой 15/15', 'pack': '25 шт'},
        ]
    },
    'fittings_traps_angle': {
        'title': 'Трапы угловые ПП 50 мм',
        'icon': 'fa-water',
        'color': '#ff6b00',
        'image': 'fitting-trap-angle.jpg',
        'product_list': [
            {'name': 'Трап угловой ПП 50 мм 10/10', 'spec': 'угловой 10/10', 'pack': '25 шт'},
            {'name': 'Трап угловой ПП 50 мм 15/15', 'spec': 'угловой 15/15', 'pack': '25 шт'},
        ]
    },
    'fittings_clamps': {
        'title': 'Хомуты ПП',
        'icon': 'fa-grip-vertical',
        'color': '#ff6b00',
        'image': 'fitting-clamp.jpg',
        'product_list': [
            {'name': 'Хомут ПП 160 мм', 'spec': '160 мм', 'pack': '50 шт'},
            {'name': 'Хомут ПП 50 мм', 'spec': '50 мм', 'pack': '100 шт'},
            {'name': 'Хомут эконом ПП 110 мм', 'spec': 'эконом 110 мм', 'pack': '100 шт'},
            {'name': 'Хомут эконом ПП 50 мм', 'spec': 'эконом 50 мм', 'pack': '100 шт'},
        ]
    },
    'fittings_transitions': {
        'title': 'Переходы ПП (бутылки)',
        'icon': 'fa-exchange-alt',
        'color': '#ff6b00',
        'image': 'fitting-transition.jpg',
        'product_list': [
            {'name': 'Переход ПП 110-50 бутылка', 'spec': '110-50', 'pack': '50 шт'},
            {'name': 'Переход ПП 160-110 бутылка', 'spec': '160-110', 'pack': '16 шт'},
        ]
    },
    'fittings_rubber': {
        'title': 'Переходы резиновые',
        'icon': 'fa-exchange-alt',
        'color': '#ff6b00',
        'image': 'fitting-rubber.jpg',
        'product_list': [
            {'name': 'Переход резиновый 110/124', 'spec': 'резиновый', 'pack': '100 шт'},
        ]
    },
    'fittings_cassettes': {
        'title': 'Кассеты ПП',
        'icon': 'fa-boxes',
        'color': '#ff6b00',
        'image': 'fitting-cassette.jpg',
        'product_list': [
            {'name': 'Кассета ПП 110 мм (10 мест)', 'spec': '10 мест', 'pack': '210 шт'},
            {'name': 'Кассета ПП 110 мм (6 мест)', 'spec': '6 мест', 'pack': '70 шт'},
            {'name': 'Кассета ПП 160 мм', 'spec': '160 мм', 'pack': '400 шт'},
            {'name': 'Кассета ПП 50 мм', 'spec': '50 мм', 'pack': '500 шт'},
        ]
    },
    'fittings_check_valve': {
        'title': 'Обратный клапан ПП 50 мм',
        'icon': 'fa-valve',
        'color': '#ff6b00',
        'image': 'fitting-check-valve.jpg',
        'product_list': [
            {'name': 'Обратный клапан ПП 50 мм', 'spec': '50 мм', 'pack': '1 шт'},
        ]
    },
}

# Галерея
GALLERY = [
    {'image': 'pipe-red-110mm.jpg', 'title': 'Трубы НПВХ рыжие SN2, SN4, SN8'},
    {'image': 'pipe-gray-110mm.jpg', 'title': 'Трубы НПВХ серые для внутренней канализации'},
    {'image': 'fittings-1.jpg', 'title': 'Фитинги ПП: отводы, тройники, крестовины'},
]


@app.route('/')
def index():
    """Главная страница"""
    current_date = datetime.now().strftime("%d.%m.%Y")
    return render_template('index.html',
                           products=PRODUCTS,
                           gallery=GALLERY,
                           current_date=current_date)


@app.route('/submit_lead', methods=['POST'])
def submit_lead():
    """Отправка заявки на email"""
    try:
        data = request.get_json()

        name = data.get('name', 'Не указано')
        phone = data.get('phone', 'Не указано')
        product = data.get('product', 'Не указано')
        quantity = data.get('quantity', '1')
        email = data.get('email', 'Не указан')
        comment = data.get('comment', 'Не указан')

        # Формируем письмо
        subject = f"Новая заявка с сайта Flextron от {name}"

        html_body = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: #ff6b00; color: white; padding: 10px; text-align: center; }}
                .content {{ padding: 20px; background: #f5f5f5; }}
                .field {{ margin: 10px 0; }}
                .label {{ font-weight: bold; color: #333; }}
                .value {{ color: #555; }}
                .footer {{ background: #333; color: white; padding: 10px; text-align: center; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2>📋 НОВАЯ ЗАЯВКА С САЙТА FLEXTRON</h2>
                </div>
                <div class="content">
                    <div class="field"><span class="label">👤 Имя:</span> <span class="value">{name}</span></div>
                    <div class="field"><span class="label">📞 Телефон:</span> <span class="value">{phone}</span></div>
                    <div class="field"><span class="label">📧 Email:</span> <span class="value">{email}</span></div>
                    <div class="field"><span class="label">🏭 Товар:</span> <span class="value">{product}</span></div>
                    <div class="field"><span class="label">📦 Количество:</span> <span class="value">{quantity} шт</span></div>
                    <div class="field"><span class="label">💬 Комментарий:</span> <span class="value">{comment}</span></div>
                    <div class="field"><span class="label">⏰ Время:</span> <span class="value">{datetime.now().strftime('%H:%M %d.%m.%Y')}</span></div>
                </div>
                <div class="footer">
                    <p>Письмо сгенерировано автоматически.</p>
                </div>
            </div>
        </body>
        </html>
        """

        # Создаем сообщение
        msg = MIMEMultipart()
        msg['From'] = EMAIL_LOGIN
        msg['To'] = EMAIL_TO
        msg['Subject'] = subject

        msg.attach(MIMEText(html_body, 'html'))

        # Отправляем email
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(EMAIL_LOGIN, EMAIL_PASSWORD)
            server.send_message(msg)

        print(f"✅ Заявка отправлена на email: {EMAIL_TO}")

        return jsonify({
            'success': True,
            'message': 'Заявка успешно отправлена! Менеджер свяжется с вами.'
        })

    except Exception as e:
        print(f"❌ Ошибка отправки email: {e}")
        # Всё равно возвращаем успех, чтобы пользователь не видел ошибку
        return jsonify({
            'success': True,
            'message': 'Заявка принята! Менеджер свяжется с вами.'
        })

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)