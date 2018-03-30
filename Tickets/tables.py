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

    class Meta:
        model = Ticket
        sequence = ('date', 'event', 'venue_Name', 'start_Time', 'add')
        attrs = {'class': 'ticket'}


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
