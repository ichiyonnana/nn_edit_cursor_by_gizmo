# 最小構成のオペレーターとメニュー追加

import bpy
import types

from .core import *

bl_info = {
    # アドオンの名前 [str]
    "name": "NN Edit Cursor By Gizmo",
    # アドオンの作者 [str]
    "author": "ichiyonnana",
    # アドオンのバージョン [tuple]
    "version": (0, 0),
    # アドオンが動作するBlender本体の最古のバージョン。
    # ここに指定されたバージョンより古いBlenderでアドオンを
    # インストールすると警告が出る [tuple]
    "blender": (2, 83, 0),
    # アドオンが提供する機能が存在する場所 [str]
    "location": "View3D > Object",
    # アドオンの説明文 [str]
    "description": "test addon",
    # アドオン使用時の注意点、バグ情報等 [str]
    "warning": "",
    # アドオンのサポートレベル [str]
    "support": 'TESTING',
    # アドオンに関連する情報が得られるサイトのURL（ドキュメントサイト）
    # [str]
    "wiki_url": "",
    # アドオンに関するサポートサイトのURL [str]
    "tracker_url": "",
    # アドオンのカテゴリ [str]
    "category": "Object"
}

# 登録クラスリスト
classes = [v for k,v in locals().copy().items() if hasattr(v, "bl_label")]

# アドオン有効化
def register():
    # オペレーター登録
    for c in classes:
        try:
            bpy.utils.register_class(c)
        except:
            pass

    #メッセージ
    print("nncursorutil add-on is enabled")

# アドオン無効化
def unregister():
    # オペレーター削除
    for c in classes:
        bpy.utils.unregister_class(c)
    # メッセージ
    print("nncursorutil add-on is disabled")
