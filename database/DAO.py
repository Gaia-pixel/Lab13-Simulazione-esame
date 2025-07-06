
from database.DB_connect import DBConnect
from model.driver import Driver


class DAO():
    @staticmethod
    def get_years():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT distinct s.`year`
                        FROM seasons s
                        """
            cursor.execute(query)

            for row in cursor:
                result.append(row['year'])

            cursor.close()
            cnx.close()

        return result

    @staticmethod
    def getAllNodes(anno):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT distinct d.*
                        FROM drivers d, races r, results re
                        WHERE d.driverId = re.driverId 
                                and r.raceId = re.raceId
                                and re.`position` is not null
                                and r.`year` = %s
                            """
            cursor.execute(query, (anno,))

            for row in cursor:
                result.append(Driver(**row))

            cursor.close()
            cnx.close()

        return result

    @staticmethod
    def getArchi1(anno):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT re.driverId, re.raceId, re.`position`
                        FROM results re, races r 
                        WHERE re.raceId = r.raceId
                                and r.`year` = %s
                                and re.`position` is not null
                                """
            cursor.execute(query, (anno,))

            for row in cursor:
                result.append((row['driverId'], row['raceId'], row['position']))

            cursor.close()
            cnx.close()

        return result

    @staticmethod
    def getArchi2(anno):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT t1.driverId as d1, t2.driverId as d2, count(*) as peso
                        FROM (SELECT re.driverId, re.raceId, re.`position`
                                FROM results re, races r 
                                WHERE re.raceId = r.raceId
                                and r.`year` = %s
                                and re.`position` is not null) t1, 
                                (SELECT re.driverId, re.raceId, re.`position`
                                FROM results re, races r 
                                WHERE re.raceId = r.raceId
                                and r.`year` = %s
                                and re.`position` is not null) t2
                        WHERE t1.raceId = t2.raceId 
                                and t1.`position` < t2.`position`
                        GROUP BY t1.driverId, t2.driverId
                                    """
            cursor.execute(query, (anno, anno))

            for row in cursor:
                result.append((row['d1'], row['d2'], row['pesor']))

            cursor.close()
            cnx.close()

        return result






