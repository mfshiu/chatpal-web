import calendar
import datetime
from datetime import datetime as dt
from datetime import timedelta
from flask import Blueprint, jsonify, redirect, render_template, request, url_for

import helper


setting_app = Blueprint('setting', __name__, static_folder='static')
logger = helper.get_logger()


def get_dates_between(start_date_str, end_date_str, weekdays=None):
    start_date = dt.strptime(start_date_str, '%Y-%m-%d')
    end_date = dt.strptime(end_date_str, '%Y-%m-%d')

    date_list = []

    while start_date <= end_date:
        if weekdays:
            if start_date.weekday() in weekdays:
                date_list.append(start_date.strftime('%Y-%m-%d'))
        else:
            date_list.append(start_date.strftime('%Y-%m-%d'))
        start_date += timedelta(days=1)
    
    return date_list


def get_dates(day_type, start_date, end_date):
    dates = []
    if day_type == "weekday":
        dates = get_dates_between(start_date, end_date, (0,1,2,3,6))
    elif day_type == "weekend":
        dates = get_dates_between(start_date, end_date, (4,5))
    elif day_type == "special":
        dates = get_dates_between(start_date, end_date)

    return dates


def query_prices(room_id:str, year:int):
    cmd = f'''select to_char(room_date, 'YYYY-MM-DD') room_date, price
from "RoomPrice" 
where room_id = %s
    and EXTRACT(YEAR FROM room_date) = %s
order by room_date;'''
    # logger.debug(f"cmd: {cmd}, params: {(room_id, year)}")
    prices = helper.execute_query_as_dict_list(cmd, (room_id, year))
    # logger.debug(f"prices: {prices}")
    
    return prices


def update_prices(room_id:str, dates, price):
    cmd_delete = f'''delete from "RoomPrice" 
where room_id = %s
    and room_date = ANY(%s::date[])'''
    # logger.debug(f"cmd_delete: {cmd_delete}")

    cmd_insert = f'''insert into "RoomPrice" 
(room_id, room_date, price) values (%s, %s, %s)'''
    
    cmds = [(cmd_delete, (room_id, dates))]
    for date_str in dates:
        cmds.append((cmd_insert, (room_id, date_str, price)))
    
    helper.execute_commands(cmds)

   
@setting_app.route('/price')
def price():
    return redirect("/price/1/J1")
     
   
@setting_app.route('/price/<zone_id>')
def price_zone(zone_id:int):
    rooms = helper.get_rooms(zone_id)
    return redirect(f"/price/{zone_id}/{rooms[0]['room_id']}")
    
    
@setting_app.route('/price/<zone_id>/<room_id>')
def price_room(zone_id:int, room_id:str):
    room_id = room_id.upper()
    year = helper.parse_int(request.args.get('year'), dt.now().year)

    prices = {}
    for m in range(1, 13):
        prices.update({f'{year:04}-{m:02}-{i:02}': 88888 for i in range(1, 32)})
    room_prices = query_prices(room_id, year)
    for a in room_prices:
        prices[a['room_date']] = a['price']
    # logger.debug(f"prices: {prices}")
    # logger.debug(f"room_prices: {room_prices}")
    
    return render_template('/price.html',
        zone_id=zone_id,
        room_id=room_id,
        zones=helper.get_zones(),
        rooms=helper.get_rooms(zone_id),
        year=year,
        prices=prices,
        datetime=datetime,
        calendar=calendar
    )


@setting_app.route('/set_price', methods=['POST'])
def set_price():
    day_type = request.form['dayType']
    room_id = request.form['roomID']
    start_date = request.form['startDate']
    end_date = request.form['endDate']
    price = helper.parse_int(request.form['price'], -1)
    logger.info(f"day_type: {day_type}, start_date: {start_date}, end_date: {end_date}, price: {price}")

    def get_error():
        error = None
        if price <= 0 and price > 88888:
            error = f"Invalid price {price}"

        return error

    if error := get_error():
        response = {
            'status': 'failed',
            'message': error
        }
    else:
        if start_date > end_date:
            start_date, end_date = end_date, start_date
        dates = get_dates(day_type, start_date, end_date)
        if dates:
            update_prices(room_id, dates, price)

        response = {
            'status': 'success',
            'message': f'Set "{day_type}" from the frontend!'
        }

    return jsonify(response)
 