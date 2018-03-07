import django_tables2 as tables


ticket_date = ''' <div class="dateSquare">
                    <h3>MAR</h3>
                    <h3>10</h3>
                    <h3>2018</h3>
                  </div> '''

add_ticket = '''<button class="btn btn-secondary">Add to Cart</button>'''


class TicketTable(tables.Table):
    date = tables.TemplateColumn(ticket_date, verbose_name=" ", orderable=False)
    event = tables.Column(" ", orderable=False)
    location = tables.Column(" ", orderable=False)
    time = tables.Column(" ", orderable=False)
    add = tables.TemplateColumn(add_ticket, verbose_name=" ", orderable=False)

    class Meta:
        attrs = {'class': 'ticket'}
