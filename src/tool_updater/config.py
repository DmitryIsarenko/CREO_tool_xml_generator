# абсолютный путь до папки, в которой планируется генерировать xml для всего инструмента
# в конце не должно быть слэша
abs_path_to_dir_where_to_create_tool_xmls = r"w:\SOFT\Tool_generator_python_2025\temp_dir_for_tools\v03 2025-04-22"
# abs_path_to_dir_where_to_create_tool_xmls = r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path"


# часть абсолютного пути, которая определяет путь ДО папки, где лежит сам проект
# в конце не должно быть слэша
abs_path_to_dir_where_project_is_located = r"w:\SOFT\Tool_generator_python_2025\tool_base"
# abs_path_to_dir_where_project_is_located = r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base"




MAX_RPM = 18000

NDIGITS_FEED = 3
NDIGITS_FEED_PER_UNIT = 5
NDIGITS_AXIAL_FEED = 3
NDIGITS_RADIAL_FEED = 3
NDIGITS_SPINDLE = 2
NDIGITS_SURFACE_SPEED = 3

vc_min_or_max = 0  # 0 для минимальной скорости, -1 для максимальной, если их указано две или более

finishing_roughing_options = {
    "roughing": {
        "vc_modifier": 1,  # Множитель для подачи (и на зуб, и на оборот)
        "feed_rate_multiplier": 0.6,  # Множитель для скорости резания
    },
    "finishing": {
        "vc_modifier": 1.2,
        "feed_rate_multiplier": 0.4,
    },
}

# GEOMETRY DATA CATALOGUE
key_order_no = "order_no"
key_body_len = "full_body_len"
key_body_diam = "full_body_diam"
key_flute_len = "flute_len"
key_flute_diam = "flute_diam"
key_lowering_len = "neck_len"
key_lowering_diam = "neck_diam"
key_edge_radius = "cutting_edge_rad"
key_edge_chamfer = "cutting_edge_chamfer"
key_shank_diam = "shank_diam"
key_num_of_teeth = "num_of_teeth"

# CUT DATA CATALOGUE
# main key. Value will be dictionary with subkeys
key_iso_P = "iso_P"  # От низколегированных до высоколегированных и стальное литье
key_iso_M = "iso_M"  # Вся нержавейка. 12% хрома и больше
key_iso_K = "iso_K"  # Все чугуны. Серые, ковкие, с шаровидным, вермикулярным графитом, отпущенный ковкий
key_iso_N = "iso_N"  # Цветные металлы. Алюминий, медь, латунь, бронза...
key_iso_S = "iso_S"  # Жаропрочные сплавы. Высоколегированные материалы на основе железа, никеля, кобальта и титана
key_iso_H = "iso_H"  # Матералы высокой твердости. Стали 45-65HRC и отбеленный чугун 400-600HB

# Subkeys for cutdata catalogue
key_vc = "Vc"  # Скорость резания
key_z = "z"  # Число режущих кромок или пластин
key_fn = "Fn"  # Подача на мм/оборот
key_fz = "Fz"  # Подача мм/зуб
key_f = "F"  # Подача мм/мин
key_ae = "Ae"  # Радиальная подача (engagement)
key_ap = "Ap"  # Осевая подача (profile)

mfg_materials_dict = {
    "ALUMINIUM": key_iso_N,
    "STEEL-20": key_iso_P,
    "12X18H10T": key_iso_M,
    "Не указано": key_iso_M,
}

lst_of_material_groups: list[str] = [
    key_iso_P,
    key_iso_M,
    key_iso_K,
    key_iso_N,
    key_iso_S,
    key_iso_H,
]

# ER collet sizes
collet_sizes = {
    "ER16": {
        "max_diam": 10,
        "nut_diam": 28,
    },
    "ER20": {
        "max_diam": 13,
        "nut_diam": 34,
    },
    "ER25": {
        "max_diam": 16,
        "nut_diam": 42,
    },
    "ER32": {
        "max_diam": 20,
        "nut_diam": 50,
    },
    "ER40": {
        "max_diam": 26,
        "nut_diam": 63,
    },
    "ER50": {
        "max_diam": 40,
        "nut_diam": 90,
    },
}

turnmill_holders_safe_lengths = {
    "TM_X_": {
        "max_safe_length": 180,
        "length_taken_by_holder": 94,
    },
    "TM_X_L_": {
        "max_safe_length": 180,
        "length_taken_by_holder": 101,
    },
    "TM_Z_1_": {
        "max_safe_length": 10000,
        "length_taken_by_holder": 0,
    },
    "TM_Z_2_": {
        "max_safe_length": 10000,
        "length_taken_by_holder": 0,
    },
    "TM_Z_SUB_": {
        "max_safe_length": 160,
        "length_taken_by_holder": 90.5,
    },
    "T_Z_ER_": {
        "max_safe_length": 10000,
        "length_taken_by_holder": 0,
    },
    "T_Z_SUB_ER_": {
        "max_safe_length": 160,
        "length_taken_by_holder": 76,
    },
    "T_Z_": {
        "max_safe_length": 10000,
        "length_taken_by_holder": 0,
    },
    "T_Z_SUB_": {
        "max_safe_length": 160,
        "length_taken_by_holder": 42.5,
    },
    "T_Z_F2_": {
        "max_safe_length": 10000,
        "length_taken_by_holder": 0,
    },
}
