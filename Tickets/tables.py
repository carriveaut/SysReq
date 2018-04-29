import django_tables2 as tables
from .models import Ticket


ticket_date = ''' <div class="dateSquare">
                    {% if record.start_Date.month == 1 %}
                        <h3>JAN</h3>
                    {% elif record.start_Date.month == 2 %}
                        <h3>FEB</h3>
                    {% elif record.start_Date.month == 3 %}
                        <h3>MAR</h3> 
                    {% elif record.start_Date.month == 4 %}
                        <h3>APR</h3>
                    {% elif record.start_Date.month == 5 %}
                        <h3>MAY</h3>
                    {% elif record.start_Date.month == 6 %}
                        <h3>JUN</h3>
                    {% elif record.start_Date.month == 7 %}
                        <h3>JUL</h3>
                    {% elif record.start_Date.month == 8 %}
                        <h3>AUG</h3>
                    {% elif record.start_Date.month == 9 %}
                        <h3>SEP</h3>
                    {% elif record.start_Date.month == 10 %}
                        <h3>OCT</h3> 
                    {% elif record.start_Date.month == 11 %}
                        <h3>NOV</h3>
                    {% elif record.start_Date.month == 12 %}
                        <h3>DEC</h3>                          
                    {% endif %}
                    <h3>{{ record.start_Date.day }}</h3>
                    <h3>{{ record.start_Date.year }}</h3>
                  </div> '''

add_ticket = '''<input class="myHidden" id="ticketID" name="ticketID" type="hidden" value="{{ record.id }}"/>
                <a href="{{ record.id }}" role="button" class="btn btn-secondary myButton" id="btn_ticket" name="btn_ticket">View Ticket</a>'''

add_cart = '''<input class="myHidden" id="ticketID" name="ticketID" type="hidden" value="{{ record.id }}"/>
              <button id="add_cart" name="add_cart" class="btn btn-secondary add_cart">Add to Cart</button>'''

add_qty = '''<input type="number" name="qty" id="qty" class="form-control text-center" value="1">'''


class TicketTable(tables.Table):
    date = tables.TemplateColumn(ticket_date, verbose_name=" ", orderable=False)
    add = tables.TemplateColumn(add_ticket, verbose_name=" ", orderable=False)
    id = tables.Column(visible=False)
    classification = tables.Column(visible=False)
    start_Date = tables.Column(visible=False)
    status = tables.Column(visible=False)
    event = tables.Column(" ", attrs={'td': {'width': '35%'}}, orderable=False)
    venue_Name = tables.Column(" ", orderable=False)
    venue_Info = tables.Column(visible=False)
    start_Time = tables.Column(" ", orderable=False)
    qty = tables.Column(visible=False)
    image_Url = tables.Column(visible=False)
    price = tables.Column(visible=False)
    on_sale = tables.Column(visible=False)
    sale_price = tables.Column(visible=False)

    class Meta:
        model = Ticket
        sequence = ('date', 'event', 'venue_Name', 'start_Time', 'add')
        attrs = {'class': 'ticket'}


class HappeningSoonTable(tables.Table):
    date = tables.TemplateColumn(ticket_date, verbose_name=" ", orderable=False)
    add = tables.TemplateColumn(add_ticket, verbose_name=" ", orderable=False)
    id = tables.Column(visible=False)
    classification = tables.Column(" ", attrs={'td': {'width': '15%'}}, orderable=False)
    start_Date = tables.Column(visible=False)
    status = tables.Column(visible=False)
    event = tables.Column(" ", attrs={'td': {'width': '25%'}}, orderable=False)
    venue_Name = tables.Column(" ", orderable=False)
    venue_Info = tables.Column(visible=False)
    start_Time = tables.Column(" ", orderable=False)
    qty = tables.Column(visible=False)
    image_Url = tables.Column(visible=False)
    price = tables.Column(visible=False)
    on_sale = tables.Column(visible=False)
    sale_price = tables.Column(visible=False)

    class Meta:
        model = Ticket
        sequence = ('date', 'classification', 'event', 'venue_Name', 'start_Time', 'add')
        attrs = {'class': 'ticket'}


class DealsTable(tables.Table):
    date = tables.TemplateColumn(ticket_date, verbose_name=" ", orderable=False)
    add = tables.TemplateColumn(add_cart, verbose_name=" ", orderable=False)
    add_qty = tables.TemplateColumn(add_qty, verbose_name=" ", orderable=False)
    id = tables.Column(visible=False)
    classification = tables.Column(" ", orderable=False)
    start_Date = tables.Column(visible=False)
    status = tables.Column(visible=False)
    event = tables.Column(" ", attrs={'td': {'width': '25%'}}, orderable=False)
    venue_Name = tables.Column(" ", orderable=False)
    venue_Info = tables.Column(visible=False)
    start_Time = tables.Column(" ", orderable=False)
    qty = tables.Column(visible=False)
    image_Url = tables.Column(visible=False)
    price = tables.Column(visible=False)
    on_sale = tables.Column(visible=False)
    sale_price = tables.Column(" ", attrs={'td': {'style': 'color: red; font-weight: bold;'}}, orderable=False)

    class Meta:
        model = Ticket
        sequence = ('date', 'classification', 'event', 'venue_Name', 'sale_price', 'start_Time', 'add_qty', 'add')
        attrs = {'class': 'ticket', 'id': 'deals'}


class SuggestionTable(tables.Table):
    date = tables.TemplateColumn(ticket_date, verbose_name=" ", orderable=False)
    add = tables.TemplateColumn(add_cart, verbose_name=" ", orderable=False)
    add_qty = tables.TemplateColumn(add_qty, verbose_name=" ", orderable=False)
    id = tables.Column(visible=False)
    classification = tables.Column(visible=False)
    start_Date = tables.Column(visible=False)
    status = tables.Column(visible=False)
    event = tables.Column(" ", attrs={'td': {'width': '30%'}}, orderable=False)
    venue_Name = tables.Column(visible=False)
    venue_Info = tables.Column(" ", orderable=False)
    start_Time = tables.Column(" ", orderable=False, attrs={'td': {'width': '10%',
                                                                   'style': 'text-align: center;'}})
    qty = tables.Column(visible=False)
    image_Url = tables.Column(visible=False)
    price = tables.Column(" ", orderable=False, attrs={'td': {'width': '10%',
                                                              'style': 'text-align: center;'}})
    on_sale = tables.Column(visible=False)
    sale_price = tables.Column(visible=False)

    class Meta:
        model = Ticket
        sequence = ('date', 'classification', 'event', 'venue_Info', 'price', 'start_Time', 'add_qty', 'add')
        attrs = {'class': 'ticket', 'id': 'deals'}


class CheckoutTable(tables.Table):
    NameOnCard = tables.Column
    CCV = tables.Column
    CCED = tables.Column
    CCCVV = tables.Column
    BAddress = tables.Column
    BCity = tables.Column
    BState = tables.Column
    BZip = tables.Column
    ShipName = tables.Column
    ShipAddress = tables.Column
    ShipCity = tables.Column
    ShipState = tables.Column
    ShipZip = tables.Column
