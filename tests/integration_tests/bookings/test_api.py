# async def test_booking(db, authenticated_ac):
#     room_id = (await db.rooms.get_all())[0].id
#     responce = await authenticated_ac.post(
#         "/bookings/",
#         json={
#             "room_id": room_id,
#             "date_from": "2024-08-10",
#             "date_to": "2024-08-20",
#         },
#     )
#     assert responce.status_code == 200
