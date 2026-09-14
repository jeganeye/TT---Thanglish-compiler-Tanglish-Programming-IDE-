"""
Tanglish Programming Language Compiler & Runtime Engine
Created for Diploma Final Year Project
SRKV PTC Coimbatore
"""

import re
import sys
import os
import io
import math
import time
import random
import json
import datetime
import traceback
import tokenize

# Windows-safe readline import
try:
    import readline
except ImportError:
    readline = None

# Base Tanglish keywords and their Python equivalents
KEYWORDS = {
    # Control flow and basic keywords
    "eluthu": "print",
    "enna": "if",
    "illana": "else",
    "varu": "def",
    "mudivu": "return",
    "neram": "while",            # While loop
    "payan": "for",
    "thodar": "continue",
    "niruthu": "break",
    "serthu": "import",
    "mugavari": "from",
    "vera": "as",
    "sirandha": "class",
    "self": "self",
    "veruppu": "pass",
    "sollu": "raise",
    "sindhanaiselutham": "try",
    "thavaruselutham": "except",
    "mudikirathu": "finally",
    "maippu": "with",
    "illainu": "elif",
    "sila": "lambda",
    "unmai": "True",
    "poi": "False",
    "ondruumillai": "None",
    "onrum_illai": "None",
    "ezhuthapadum": "global",
    "akkam": "nonlocal",
    "idam": "del",
    "thodarbu": "assert",
    "vilakku": "not",
    "athuvaaga": "and",
    "allathu": "or",
    "maari": "is",
    "udaya": "in",
    "vaangu": "input",
    
    # Data types
    "saram": "str",              # String (சரம்)
    "enn": "int",                # Integer (எண்)
    "midhaenn": "float",         # Float (மிதஎண்)
    "ulmai": "bool",             # Boolean (உள்மை)
    "pattial": "list",           # List (பட்டியல்)
    "agarathi": "dict",          # Dictionary (அகராதி)
    "thoguthy": "set",           # Set (தொகுதி)
    "urumaru": "tuple",          # Tuple (உருமாறா)
    
    # Type conversion functions
    "saram_akku": "str",         # Convert to string
    "enn_akku": "int",           # Convert to integer
    "midhaenn_akku": "float",    # Convert to float
    "ulmai_akku": "bool",        # Convert to boolean
    "pattial_akku": "list",      # Convert to list
    "agarathi_akku": "dict",     # Convert to dictionary
    "thoguthy_akku": "set",      # Convert to set
    "urumaru_akku": "tuple",     # Convert to tuple
    
    # Common methods and functions
    "idaipadu": "join",          # String join
    "piri": "split",             # String split
    "maatru": "replace",         # String replace
    "serkkavum": "append",       # List append
    "neekku": "remove",          # List remove
    "seruhu": "insert",          # List insert
    "saavigal": "keys",          # Dictionary keys
    "mathippugal": "values",     # Dictionary values
    "inaikal": "items",          # Dictionary items
    "neelamm": "len",            # Length function
    "varisaipadu": "sorted",     # Sorted function
    "vaagai": "type",            # Type function
    "madippu": "value"           # Value
}

# Tamil Standard Library (தமிழ் நிலையான நூலகம்)
TAMIL_STD_LIB = {
    # Module names (Note: "kaalam" or "neram_mod" used for time module to avoid conflict with "neram" which is "while")
    "kanitham": "math",           # Math module (கணிதம்)
    "seyalmurai": "os",           # OS module (செயல்முறை)
    "kaalam": "time",             # Time module (நேரம்/காலம்)
    "neram_mod": "time",          # Time module alias
    "saralvadivam": "re",         # Regular expressions (சரல் வடிவம்)
    "elamai": "random",           # Random module (ஏலமை)
    "kopu": "io",                 # IO module (கோப்பு)
    "json_tharavagam": "json",    # JSON module (JSON தரவகம்)
    "valai": "urllib",            # URL lib (வலை)
    "pathivu": "logging",         # Logging (பதிவு)
    "kural": "sys",               # System (கூறல்)
    "thoguppu": "collections",    # Collections (தொகுப்பு)
    "kuyidu": "pickle",           # Pickle (குயிடு)
    "kurukku": "threading",       # Threading (குறுக்கு)
    "niralakki": "datetime",      # DateTime (நிரலாக்கி)
    "pathudai": "pathlib",        # Pathlib (பாதுடை)
    "kurippu": "csv",             # CSV (குறிப்பு)
    "zippu": "zipfile",           # Zipfile (ஜிப்பு)
    "thadai": "socket",           # Socket (தடை)
    "katturai": "argparse",       # Argparse (கட்டுரை)
    "sorsodigai": "itertools",    # Itertools (சொற்சோடிகை)
    
    # Math functions
    "kanitham_sin": "math.sin",
    "kanitham_cos": "math.cos",
    "kanitham_tan": "math.tan",
    "kanitham_sqrt": "math.sqrt",
    "kanitham_log": "math.log",
    "kanitham_exp": "math.exp",
    "kanitham_pi": "math.pi",
    "kanitham_e": "math.e",
    "kanitham_floor": "math.floor",
    "kanitham_ceil": "math.ceil",
    "kanitham_abs": "abs",
    "kanitham_pow": "pow",
    "kanitham_round": "round",
    
    # Time functions
    "neram_thoongu": "time.sleep",
    "neram_ipothu": "time.time",
    "neram_ctime": "time.ctime",
    "neram_strftime": "time.strftime",
    
    # OS functions
    "seyalmurai_pathai": "os.path",
    "seyalmurai_adaivu": "os.listdir",
    "seyalmurai_remove": "os.remove",
    "seyalmurai_mkdir": "os.mkdir",
    "seyalmurai_rmdir": "os.rmdir",
    "seyalmurai_rename": "os.rename",
    "seyalmurai_getenv": "os.getenv",
    "seyalmurai_system": "os.system",
    "seyalmurai_chdir": "os.chdir",
    "seyalmurai_getcwd": "os.getcwd",
    
    # Random functions
    "elamai_enn": "random.randint",
    "elamai_thervu": "random.choice",
    "elamai_kalavai": "random.shuffle",
    "elamai_midha": "random.random",
    "elamai_uniform": "random.uniform",
    
    # File operations
    "kopu_thirappu": "open",
    "kopu_padippu": "read",
    "kopu_ezhuthu": "write",
    "kopu_moodu": "close",
    
    # String operations
    "saram_replace": "replace",
    "saram_find": "find",
    "saram_split": "split",
    "saram_join": "join",
    "saram_strip": "strip",
    "saram_upper": "upper",
    "saram_lower": "lower",
    "saram_startswith": "startswith",
    "saram_endswith": "endswith",
    
    # Regular expressions
    "saralvadivam_poruthu": "re.match",
    "saralvadivam_thedu": "re.search",
    "saralvadivam_maatru": "re.sub",
    "saralvadivam_piri": "re.split",
    "saralvadivam_anaithu": "re.findall",
    "saralvadivam_compile": "re.compile",
    
    # JSON operations
    "json_parse": "json.loads",
    "json_stringify": "json.dumps",
    "json_kopu_padippu": "json.load",
    "json_kopu_ezhuthu": "json.dump",
    
    # System functions
    "kural_veliyeru": "sys.exit",
    "kural_path": "sys.path",
    "kural_argv": "sys.argv",
    "kural_version": "sys.version",
    "kural_platform": "sys.platform",
    
    # DateTime functions
    "niralakki_ipothu": "datetime.datetime.now",
    "niralakki_date": "datetime.date",
    "niralakki_time": "datetime.time",
    "niralakki_delta": "datetime.timedelta",
    
    # Collections
    "thoguppu_counter": "collections.Counter",
    "thoguppu_defaultdict": "collections.defaultdict",
    "thoguppu_deque": "collections.deque",
    "thoguppu_namedtuple": "collections.namedtuple",
    
    # URL operations
    "valai_request": "urllib.request.urlopen",
    "valai_parse": "urllib.parse.urlparse",
    "valai_quote": "urllib.parse.quote",
    "valai_unquote": "urllib.parse.unquote",
    
    # Logging
    "pathivu_amaipu": "logging.basicConfig",
    "pathivu_debug": "logging.debug",
    "pathivu_info": "logging.info",
    "pathivu_warning": "logging.warning",
    "pathivu_error": "logging.error",
    "pathivu_critical": "logging.critical",
    
    # Path operations
    "pathudai_path": "pathlib.Path",
    "pathudai_home": "pathlib.Path.home",
    "pathudai_exists": "pathlib.Path.exists",
    "pathudai_mkdir": "pathlib.Path.mkdir",
    
    # CSV operations
    "kurippu_reader": "csv.reader",
    "kurippu_writer": "csv.writer",
    "kurippu_dictreader": "csv.DictReader",
    "kurippu_dictwriter": "csv.DictWriter",
    
    # Zip operations
    "zippu_thirappu": "zipfile.ZipFile",
    "zippu_extract": "extractall",
    "zippu_serukku": "write",
    
    # Socket operations
    "thadai_socket": "socket.socket",
    "thadai_connect": "connect",
    "thadai_bind": "bind",
    "thadai_listen": "listen",
    "thadai_accept": "accept",
    
    # Itertools
    "sorsodigai_cycle": "itertools.cycle",
    "sorsodigai_count": "itertools.count",
    "sorsodigai_chain": "itertools.chain",
    "sorsodigai_combinations": "itertools.combinations",
    "sorsodigai_permutations": "itertools.permutations"
}

# Tamil data visualization with matplotlib
TAMIL_VISUALIZATION = {
    "varaipada": "matplotlib.pyplot",       # Plotting library (வரைபடம்)
    "varaipada_paddam": "plt.figure",       # Figure (படம்)
    "varaipada_thalaippu": "plt.title",     # Title (தலைப்பு)
    "varaipada_x_label": "plt.xlabel",      # X-axis label
    "varaipada_y_label": "plt.ylabel",      # Y-axis label
    "varaipada_kodu": "plt.plot",           # Line plot (கோடு)
    "varaipada_patti": "plt.bar",           # Bar plot (பட்டி)
    "varaipada_vattam": "plt.pie",          # Pie chart (வட்டம்)
    "varaipada_sitharam": "plt.scatter",    # Scatter plot (சிதறல்)
    "varaipada_kaattu": "plt.show",         # Show plot (காட்டு)
    "varaipada_seemai": "plt.axis",         # Set axis (சீமை)
    "varaipada_grid": "plt.grid",           # Grid (கட்டம்)
    "varaipada_save": "plt.savefig",        # Save figure (சேமி)
    "varaipada_close": "plt.close",         # Close figure (மூடு)
    "varaipada_legend": "plt.legend",       # Legend (விளக்கம்)
    "varaipada_vannangal": "plt.colors",    # Colors (வண்ணங்கள்)
}

# Tamil data analysis with pandas and numpy
TAMIL_DATA_ANALYSIS = {
    "tharavu": "pandas",                    # Pandas (தரவு)
    "tharavu_padippu": "pd.read_csv",       # Read CSV (படிப்பு)
    "tharavu_ezhuthu": "to_csv",            # Write CSV (எழுது)
    "tharavu_adavani": "DataFrame",         # DataFrame (அட்டவணை)
    "tharavu_varisai": "Series",            # Series (வரிசை)
    "tharavu_thervu": "loc",                # Selection (தேர்வு)
    "tharavu_vadikatti": "filter",          # Filter (வடிகட்டி)
    "tharavu_kurukku": "groupby",           # Group by (குறுக்கு)
    "tharavu_serpu": "merge",               # Merge (சேர்ப்பு)
    "tharavu_pivot": "pivot_table",         # Pivot table (சுழற்சி)
    
    "enn_aani": "numpy",                    # NumPy (எண் ஆணி)
    "enn_aani_array": "np.array",           # Array (அணி)
    "enn_aani_range": "np.arange",          # Range (வரம்பு)
    "enn_aani_zeros": "np.zeros",           # Zeros (பூஜ்யங்கள்)
    "enn_aani_ones": "np.ones",             # Ones (ஒன்றுகள்)
    "enn_aani_random": "np.random",         # Random (சீரற்ற)
    "enn_aani_mean": "np.mean",             # Mean (சராசரி)
    "enn_aani_sum": "np.sum",               # Sum (கூட்டல்)
    "enn_aani_min": "np.min",               # Min (குறைந்த)
    "enn_aani_max": "np.max",               # Max (அதிக)
    "enn_aani_std": "np.std",               # Standard deviation (நிலையான விலகல்)
    "enn_aani_reshape": "reshape",          # Reshape (மறுவடிவம்)
}

# Tamil web development with Flask
TAMIL_WEB = {
    "valai_seyal": "Flask",                 # Flask (வலை செயல்)
    "valai_app": "app",                     # App (செயலி)
    "valai_route": "route",                 # Route (பாதை)
    "valai_request": "request",             # Request (கோரிக்கை)
    "valai_redirect": "redirect",           # Redirect (திருப்பு)
    "valai_render": "render_template",      # Render template (காட்சி)
    "valai_session": "session",             # Session (அமர்வு)
    "valai_url_for": "url_for",             # URL for (இணைப்பு)
    "valai_flash": "flash",                 # Flash message (செய்தி)
    "valai_run": "run",                     # Run (இயக்கு)
}

# Tamil machine learning with scikit-learn
TAMIL_ML = {
    "arivu": "sklearn",                     # Scikit-learn (அறிவு)
    "arivu_model": "model",                 # Model (மாதிரி)
    "arivu_payirchi": "fit",                # Fit/Train (பயிற்சி)
    "arivu_kanippu": "predict",             # Predict (கணிப்பு)
    "arivu_madipidu": "score",              # Score (மதிப்பீடு)
    "arivu_vaguppu": "classification",      # Classification (வகுப்பு)
    "arivu_adaivu": "regression",           # Regression (அடைவு)
    "arivu_kattam": "cluster",              # Clustering (கட்டம்)
    "arivu_pirivu": "train_test_split",     # Train-test split (பிரிவு)
    "arivu_alavidu": "metrics",             # Metrics (அளவிடு)
    "arivu_confusion": "confusion_matrix",  # Confusion matrix (குழப்ப அட்டவணை)
    "arivu_accuracy": "accuracy_score",     # Accuracy (துல்லியம்)
    "arivu_precision": "precision_score",   # Precision (பிழையின்மை)
    "arivu_recall": "recall_score",         # Recall (மீட்பு)
}

# Tamil database operations with SQLite
TAMIL_DB = {
    "tharavu_thalum": "sqlite3",            # SQLite (தரவுத்தளம்)
    "tharavu_inaippu": "connect",           # Connect (இணைப்பு)
    "tharavu_cursor": "cursor",             # Cursor (சுட்டி)
    "tharavu_execute": "execute",           # Execute (செயல்படுத்து)
    "tharavu_fetch": "fetchall",            # Fetch all (பெறு)
    "tharavu_fetch_one": "fetchone",        # Fetch one (ஒன்று பெறு)
    "tharavu_commit": "commit",             # Commit (உறுதி)
    "tharavu_close": "close",               # Close (மூடு)
}

# Tamil GUI development with Tkinter
TAMIL_GUI = {
    "kaatchi": "tkinter",                   # Tkinter (காட்சி)
    "kaatchi_jannalum": "Tk",               # Window (ஜன்னலும்)
    "kaatchi_label": "Label",               # Label (விளக்கம்)
    "kaatchi_button": "Button",             # Button (பொத்தான்)
    "kaatchi_entry": "Entry",               # Entry (உள்ளீடு)
    "kaatchi_frame": "Frame",               # Frame (சட்டம்)
    "kaatchi_menu": "Menu",                 # Menu (பட்டி)
    "kaatchi_checkbox": "Checkbutton",      # Checkbox (தேர்வுப்பெட்டி)
    "kaatchi_radio": "Radiobutton",         # Radio button (தேர்வு பொத்தான்)
    "kaatchi_listbox": "Listbox",           # Listbox (பட்டியல்பெட்டி)
    "kaatchi_canvas": "Canvas",             # Canvas (திரைச்சீலை)
    "kaatchi_mainloop": "mainloop",         # Main loop (முதன்மை சுழற்சி)
    "kaatchi_pack": "pack",                 # Pack (அடுக்கு)
    "kaatchi_grid": "grid",                 # Grid (கட்டம்)
    "kaatchi_place": "place",               # Place (இடம்)
}

# Register all modules into master KEYWORDS dictionary
KEYWORDS.update(TAMIL_STD_LIB)
KEYWORDS.update(TAMIL_VISUALIZATION)
KEYWORDS.update(TAMIL_DATA_ANALYSIS)
KEYWORDS.update(TAMIL_WEB)
KEYWORDS.update(TAMIL_ML)
KEYWORDS.update(TAMIL_DB)
KEYWORDS.update(TAMIL_GUI)

# CRITICAL FIX: Ensure 'neram' stays 'while' (loop) and is not overwritten by time module
KEYWORDS["neram"] = "while"

# Tamil error messages
ERROR_MESSAGES = {
    "SyntaxError": "தொடரியல் பிழை (SyntaxError)",
    "NameError": "பெயர் பிழை (NameError)",
    "TypeError": "வகை பிழை (TypeError)",
    "ValueError": "மதிப்பு பிழை (ValueError)",
    "IndexError": "குறியீட்டு பிழை (IndexError)",
    "KeyError": "சாவி பிழை (KeyError)",
    "AttributeError": "பண்புக்கூறு பிழை (AttributeError)",
    "ImportError": "இறக்குமதி பிழை (ImportError)",
    "ZeroDivisionError": "பூஜ்ஜியத்தால் வகுத்தல் பிழை (ZeroDivisionError)",
    "FileNotFoundError": "கோப்பு காணப்படவில்லை பிழை (FileNotFoundError)",
    "IndentationError": "உள்தள்ளல் பிழை (IndentationError)",
    "OverflowError": "மிகை நிரம்பல் பிழை (OverflowError)",
    "RuntimeError": "இயக்க நேர பிழை (RuntimeError)"
}

# Tamil code examples for learning
TAMIL_EXAMPLES = {
    "hello_world": """# வணக்கம் உலகம்
eluthu("வணக்கம் உலகம்!")
""",

    "calculator": """# எளிய கணிப்பான்
varu koottu(a, b):
    mudivu a + b

varu kazhi(a, b):
    mudivu a - b

varu perukku(a, b):
    mudivu a * b

varu vagu(a, b):
    enna b == 0:
        eluthu("பூஜ்ஜியத்தால் வகுக்க முடியாது!")
        mudivu ondruumillai
    mudivu a / b

eluthu("எளிய கணிப்பான்")
eluthu("1. கூட்டல்")
eluthu("2. கழித்தல்")
eluthu("3. பெருக்கல்")
eluthu("4. வகுத்தல்")

thervu = enn_akku(vaangu("உங்கள் தேர்வை உள்ளிடவும் (1-4): "))
enn1 = midhaenn_akku(vaangu("முதல் எண்ணை உள்ளிடவும்: "))
enn2 = midhaenn_akku(vaangu("இரண்டாவது எண்ணை உள்ளிடவும்: "))

enna thervu == 1:
    eluthu(f"முடிவு: {koottu(enn1, enn2)}")
illainu thervu == 2:
    eluthu(f"முடிவு: {kazhi(enn1, enn2)}")
illainu thervu == 3:
    eluthu(f"முடிவு: {perukku(enn1, enn2)}")
illainu thervu == 4:
    eluthu(f"முடிவு: {vagu(enn1, enn2)}")
illana:
    eluthu("தவறான தேர்வு!")
""",

    "guess_number": """# எண் ஊகிக்கும் விளையாட்டு
serthu elamai

ragasiya_enn = elamai_enn(1, 100)
mugayarchi = 0
kandu_pidikka_villai = unmai

eluthu("1 முதல் 100 வரையிலான எண்ணை ஊகிக்கவும்!")

neram kandu_pidikka_villai:
    mugayarchi += 1
    ooham = enn_akku(vaangu("உங்கள் ஊகம்: "))
    
    enna ooham < ragasiya_enn:
        eluthu("அதிகமாக ஊகிக்கவும்!")
    illainu ooham > ragasiya_enn:
        eluthu("குறைவாக ஊகிக்கவும்!")
    illana:
        kandu_pidikka_villai = poi
        eluthu(f"வாழ்த்துக்கள்! {mugayarchi} முயற்சிகளில் கண்டுபிடித்துவிட்டீர்கள்!")
""",

    "file_reader": """# கோப்பு படிப்பான்
kopu_peyar = vaangu("படிக்க வேண்டிய கோப்பின் பெயரை உள்ளிடவும்: ")

sindhanaiselutham:
    maippu kopu_thirappu(kopu_peyar, "r") vera kopu:
        ullaram = kopu.read()
        eluthu("கோப்பின் உள்ளடக்கம்:")
        eluthu("-------------------")
        eluthu(ullaram)
        eluthu("-------------------")
        
        varigal = ullaram.split("\\n")
        eluthu(f"மொத்த வரிகள்: {neelamm(varigal)}")
thavaruselutham:
    eluthu(f"பிழை: கோப்பை படிக்க முடியவில்லை '{kopu_peyar}'")
"""
}

def translate_tanglish_to_python(tanglish_code):
    """
    Translates Tanglish code to Python.
    Uses Python's tokenize module so string literals and comments are NOT modified.
    Falls back gracefully to word-boundary regex if tokenization is incomplete.
    """
    if not tanglish_code:
        return ""
    
    try:
        tokens = []
        reader = io.BytesIO(tanglish_code.encode('utf-8')).readline
        for tok in tokenize.tokenize(reader):
            # Only translate NAME tokens that are recognized Tanglish keywords
            if tok.type == tokenize.NAME and tok.string in KEYWORDS:
                py_word = KEYWORDS[tok.string]
                tokens.append((tok.type, py_word))
            else:
                tokens.append((tok.type, tok.string))
        return tokenize.untokenize(tokens).decode('utf-8')
    except Exception:
        # Fallback to regex word boundary replacement
        code = tanglish_code
        sorted_kw = sorted(KEYWORDS.items(), key=lambda x: len(x[0]), reverse=True)
        for tanglish, python in sorted_kw:
            code = re.sub(rf'\b{re.escape(tanglish)}\b', python, code)
        return code

def translate_error(error):
    """Translates Python exceptions and error messages into friendly Tamil descriptions"""
    error_type = type(error).__name__
    error_msg = str(error)
    tamil_error_type = ERROR_MESSAGES.get(error_type, error_type)
    return f"{tamil_error_type}: {error_msg}"

def get_default_namespace():
    """Generates an execution namespace with standard modules and helpers pre-loaded"""
    return {
        '__name__': '__main__',
        'math': math,
        'time': time,
        'random': random,
        're': re,
        'os': os,
        'sys': sys,
        'json': json,
        'datetime': datetime,
        'io': io,
        'neelamm': len,
        'varisaipadu': sorted,
        'vaagai': type,
        'eluthu': print,
        'saram': str,
        'enn': int,
        'midhaenn': float,
        'ulmai': bool,
        'pattial': list,
        'agarathi': dict,
        'thoguthy': set,
        'urumaru': tuple,
        'saram_akku': str,
        'enn_akku': int,
        'midhaenn_akku': float,
        'ulmai_akku': bool,
        'pattial_akku': list,
        'agarathi_akku': dict,
        'thoguthy_akku': set,
        'urumaru_akku': tuple,
    }

def execute_tanglish_code(tanglish_code, custom_namespace=None, debug=False):
    """
    Translates and executes Tanglish code.
    If custom_namespace is provided, code runs within that scope.
    """
    python_code = translate_tanglish_to_python(tanglish_code)
    if debug:
        print("Debug: Translated Python Code:\n", python_code)
        
    exec_namespace = custom_namespace if custom_namespace is not None else get_default_namespace()
    
    try:
        # First attempt eval (for single expressions like '2 + 5')
        result = eval(python_code, exec_namespace)
        return result
    except SyntaxError:
        try:
            # If not an expression, execute as statements
            exec(python_code, exec_namespace)
            return None
        except Exception as e:
            return translate_error(e)
    except Exception as e:
        return translate_error(e)

# Interactive Terminal REPL
def interactive_mode():
    print("Tanglish Interactive Mode (CTRL+C to exit)")
    print("உங்கள் தமிழ் பைதான் கோடுகளை இங்கே உள்ளிடவும்")
    print("Type 'udhavi()' for help")
    print("Try 'example(\"hello_world\")' to see a sample program")
    
    session_ns = get_default_namespace()
    session_ns["udhavi"] = lambda: print("Available keywords: " + ", ".join(list(KEYWORDS.keys())[:30]) + "...")
    session_ns["example"] = lambda name: print(TAMIL_EXAMPLES.get(name, "Example not found"))
    
    while True:
        try:
            tanglish_code = input("SOLLU THAMBI>>> ")
            if tanglish_code.strip():
                result = execute_tanglish_code(tanglish_code, custom_namespace=session_ns)
                if result is not None:
                    print(result)
        except KeyboardInterrupt:
            print("\nநன்றி! மீண்டும் சந்திப்போம்! (Thank you! See you again!)")
            break
        except Exception as e:
            print(f"Error: {e}")

# CLI Entrypoint
def main():
    if len(sys.argv) == 1:
        interactive_mode()
    elif len(sys.argv) == 2:
        file_path = sys.argv[1]
        with open(file_path, "r", encoding="utf-8") as file:
            tanglish_code = file.read()
        execute_tanglish_code(tanglish_code)
    else:
        print("Usage:")
        print("  python thanglish.py                 - Interactive mode")
        print("  python thanglish.py <filename.tn>   - Run Tanglish file")

if __name__ == "__main__":
    main()
