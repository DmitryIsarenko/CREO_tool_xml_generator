from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parents[2]
CATALOGS_DIR = PROJECT_DIR / 'src' / 'tool_updater' / 'catalogs'
OUTPUT_DIR = PROJECT_DIR / 'generated_xmls'


MAX_RPM = 18000

NDIGITS_FEED = 3
NDIGITS_FEED_PER_UNIT = 5
NDIGITS_AXIAL_FEED = 3
NDIGITS_RADIAL_FEED = 3
NDIGITS_SPINDLE = 2
NDIGITS_SURFACE_SPEED = 3

# 0 для минимальной скорости, -1 для максимальной, если их указано две или более
vc_min_or_max = 0

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
# Все чугуны. Серые, ковкие, с шаровидным, вермикулярным графитом, отпущенный ковкий
key_iso_K = "iso_K"
key_iso_N = "iso_N"  # Цветные металлы. Алюминий, медь, латунь, бронза...
# Жаропрочные сплавы. Высоколегированные материалы на основе железа, никеля, кобальта и титана
key_iso_S = "iso_S"
# Матералы высокой твердости. Стали 45-65HRC и отбеленный чугун 400-600HB
key_iso_H = "iso_H"
key_not_iso_plexiglas = "PLEXIGLAS"  # Плексиглас. У нас "стекла".
key_not_iso_pa6 = "PA6"  # Полиамид ПА6. наш обычный пластик
key_not_iso_ptte = "PTTE"  # Фторопласт
key_not_iso_brass = "BRASS"  # Латунь

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
    # "Не указано": key_iso_M,
    "HARDENED_STEEL": key_iso_H,
    "PLEXIGLAS": key_iso_M,
}
mfg_materials_dict = {
    # ISO N = Алюминий
    "ALUMINIUM": key_iso_N,
    # ISO P = Низколегированные стали
    "STEEL-20": key_iso_P,
    # ISO M - Нержавеющие стали
    "12X18H10T": key_iso_M,
    # ISO H = Закаленные стали
    "HARD-STEEL": key_iso_H,
    # ISO S = Жаропрочные сплавы
    "HEAT-RESISTANT": key_iso_S,

    # Плексигласс, для "стекол"
    "PLEXIGLAS": key_not_iso_plexiglas,
    # Полиамид
    "PA6": key_not_iso_pa6,
    # Фторопласт
    "PTTE": key_not_iso_ptte,
    # Латунь
    "BRASS": key_not_iso_brass,
}


lst_of_iso_material_groups: list[str] = [
    key_iso_P,
    key_iso_M,
    key_iso_K,
    key_iso_N,
    key_iso_S,
    key_iso_H,
]

lst_of_not_iso_material_groups: list[str] = [
    key_not_iso_brass,
    key_not_iso_pa6,
    key_not_iso_plexiglas,
    key_not_iso_ptte,
]

not_iso_materials_modifyers: dict = {
    key_not_iso_plexiglas: {
        "from_iso": key_iso_N,
        "k_Vc": 0.4,
        "k_Ae": 0.5,
        "k_Ap": 1,
        "k_Fz": 0.3,
    },
    key_not_iso_pa6: {
        "from_iso": key_iso_N,
        "k_Vc": 0.8,
        "k_Ae": 1,
        "k_Ap": 0.7,
        "k_Fz": 0.85,
    },
    key_not_iso_ptte: {
        "from_iso": key_iso_N,
        "k_Vc": 0.7,
        "k_Ae": 1,
        "k_Ap": 0.6,
        "k_Fz": 0.7,
    },
    key_not_iso_brass: {
        "from_iso": key_iso_N,
        "k_Vc": 0.6,
        "k_Ae": 1.1,
        "k_Ap": 1,
        "k_Fz": 0.75,
    },
    key_iso_H: {
        "from_iso": key_iso_P,
        "k_Vc": 0.3,
        "k_Ae": 0.4,
        "k_Ap": 0.4,
        "k_Fz": 0.4,
    },
    key_iso_S: {
        "from_iso": key_iso_M,
        "k_Vc": 0.4,
        "k_Ae": 0.5,
        "k_Ap": 0.6,
        "k_Fz": 0.7,
    },
}

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
