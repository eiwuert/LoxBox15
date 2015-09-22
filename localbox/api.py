"""
LocalBox API Implementation module
"""
from json import dumps
from re import compile as regex_compile
from os import symlink
from os.path import join

from .shares import list_share_items
from .shares import get_database_invitations
from .shares import toggle_invite_state
from .encoding import localbox_path_decoder

def exec_shares(request_handler):
    """
    Handle share information
    """
    path2 = request_handler.path.replace('/lox_api/shares/', '', 1)

    request_handler.send_response(200)
    request_handler.end_headers()

    data = list_share_items(path2)
    request_handler.wfile.write(data)

def exec_invitations(request_handler):
    """
    Handle invitation listing
    """
    request_handler.send_response(200)
    request_handler.end_headers()
    request_handler.wfile.write(get_database_invitations(request_handler.user))

def exec_invite_accept(request_handler):
    """
    Accepts/reopens an invitation to filesharing.
    """
    result = toggle_invite_state(request_handler, 'accepted')
    if result:
        request_handler.send_response(200)
    else:
        request_handler.send_response(404)
    request_handler.end_headers()

def exec_invite_reject(request_handler):
    """
    Rejects/cancels an invitation to filesharing.
    """
    result = toggle_invite_state(request_handler, 'rejected')
    if result:
        request_handler.send_response(200)
    else:
        request_handler.send_response(404)

    request_handler.end_headers()


def exec_user(request_handler):
    """
    Handle user info (or pretend to)
    """
    info = {'name': 'user', 'public_key': 'FT9CH-XVXW7',
            'private_key': 'RPR49-VDHYD', 'complete': 'No!'}
    request_handler.wfile.write(dumps(info))


def exec_files_path(request_handler):
    """
    2 POST /lox_api/files/{path}
    Upload file '{path}' naar de localbox server. {path} is een relatief file
    path met urlencoded componenten (e.g.: path/to/file%20met%20spaties).
    """
    if request_handler.command == "POST":
        print("Running files path :  2 POST /lox_api/files/{path}")
        s = "\/lox_api\/files\/.*"
        s.lstrip(".*")
        """
        A 'localbox_path' is a unix filepath with the urlencoded components.
        """
        localbox_path_decoder(s)
        request_handler.wfile.write(dumps(info))
    elif request_handler.command == "GET":
        print("Running files path :  20 GET /lox_api/files/{path}")
        s = "\/lox_api\/files\/.*"
        s.lstrip(".*")
        localbox_path_decoder(s)
        request_handler.wfile.write(dumps(info))


# 10 POST /lox_api/operations/copy
#    Kopieert een file van from_path naar to_path en retourneert of het succesvol is.
#    De volgende velden moeten bij de call aanwezig zijn.
#    - from_path: pad naar de file die gekopieert moet worden
#    - to_path: locatie waar de nieuwe file neergezet moet worden.
#    retourneert 200 in geval van succes, 404 in geval van falen.
def exec_operations_copy(request_handler):
    """
    # Kopieert een file van from_path naar to_path en retourneert of het succesvol is.
    """
    request_handler.from_path,
    request_handler.to_path
    bindpoint = configparser.get('httpd', 'bindpoint')
    user = request_handler.user

    print("Running operations copy : 10 POST /lox_api/operations/copy")
    request_handler.send_response(200)
    request_handler.end_headers()


def exec_create_share(request_handler):
    json_object = request_Handler.rfile.read()
    path2 = request_handler.path.replace('/lox_api/share_create/', '', 1)
    bindpoint = ConfigSingleton().get('filesystem', 'bindpoint')
    user = json_object.username
    myself = request_handler.user
    from_file = join(bindpoint, myself, path2)
    to_file = join(*bindpoint, user, path2)
    if exists(to_file):
        print("file exists. problem!")
    symlink(from_file, to_file)
    request_handler.send_response(200)
    request_handler.end_headers()

ROUTING_LIST = [
    (regex_compile(r"\/lox_api\/invitations"), exec_invitations),
    (regex_compile(r"\/lox_api\/invite/[0-9]+/accept"), exec_invite_accept),
    (regex_compile(r"\/lox_api\/invite/[0-9]+/reject"), exec_invite_reject),
    (regex_compile(r"\/lox_api\/user"), exec_user),
    (regex_compile(r"\/lox_api\/shares\/.*"), exec_shares),
    (regex_compile(r"\/lox_api\/files\/.*"), exec_files_path),
    (regex_compile(r"\/lox_api\/operations\/copy"), exec_operations_copy),
    (regex_compile(r"\/lox_api\/share_create\/.*")m exec_share_create),
]

