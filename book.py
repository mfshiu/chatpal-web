from flask import Blueprint, render_template

import helper


book_app = Blueprint('booking', __name__, static_folder='static')
logger = helper.get_logger()


def query_rooms(book_id:str):
    cmd = f'''select r.room_id, r.room_name, to_char(room_date, 'YYYY-MM-DD') room_date
from "BookRoom" br
join "Room" r on r.room_id=br.room_id
where book_id = %s
order by room_id, room_date;'''
    rooms = helper.execute_query_as_dict_list(cmd, (book_id,))
    
    logger.debug(f"room_orders: {rooms}")
    return rooms


def query_room_orders():
    cmd = f'''select book_id, check_in_date, check_out_date, booker_name, booker_name, 
booker_phone, booker_email, details from "BookOrder"
where check_in_date >= CURRENT_DATE
order by check_in_date desc;'''
    room_orders = helper.execute_query_as_dict_list(cmd, None)    
    
    for room_order in room_orders:
        room_order["rooms"] = query_rooms(room_order["book_id"])
    
    logger.debug(f"room_orders: {room_orders}")
    return room_orders
    
  
@book_app.route('/book')
def book():
    logger.debug("Start booking...")
    # return render_template('/book.html')
    return render_template('/book.html', room_orders=query_room_orders())
    