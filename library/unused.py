class ReservationManager(models.Manager):
    def create_reservation(self, book_reserved, book_reserved_by, book_reserved_date, book_reservation_end_date):
        bookreservation = self.create(book_reserved=book_reserved,
                                      book_reserved_by=book_reserved_by,
                                      book_reserved_date=book_reserved_date,
                                      book_reservation_end_date=book_reservation_end_date)
        return bookreservation

class BookReservation(models.Model):
    book_reserved = models.ForeignKey(Book, default=None, on_delete=models.SET_DEFAULT)
    book_reserved_by = models.ForeignKey(User, default=None, on_delete=models.SET_DEFAULT, blank=False, null=True)
    book_reserved_date = models.DateTimeField('date reserved', default=None, null=True, blank=True)
    book_reservation_end_date = models.DateTimeField('reservation end', default=None, null=True, blank=True)
    objects =  ReservationManager()
    class Meta():
        verbose_name_plural = "Reservations"
    def __str__(self):
        return self.book_reserved

        def reservebook(request, book_id):
            book = get_object_or_404(Book, id=book_id)
            book.book_reserved = True
            book.save()
            reservation_end_date = timezone.now() + timezone.timedelta(days=3)
            reservation = BookReservation.objects.create_reservation(book, request.user, timezone.now(), reservation_end_date)
            reservation.save()
            return render(request = request,
                          template_name = 'system/index.html',
                          context = {"books": Book.objects.all(),
                                     "notices":Notice.objects.all(),
                                     "from":"reservebook"})

path('<int:book_id>/reservebook/', views.reservebook, name='reservebook'),
