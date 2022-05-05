from motor.motor_asyncio import AsyncIOMotorClient

class Application:
    """
    Application 
    """
    def __init__(self, host:str = None,
                username: str = None,
                password: str = None) -> None:
        """
        host: string :> mongodb connection url
        username: string :> mongodb username
        password: string :> mongodb password

        returns: None
        
        """
        self.host = host
        self.username = username
        self.password = password

        self.client: AsyncIOMotorClient = AsyncIOMotorClient(
            host= self.host,
            username=self.username,
            password=self.password
        )

        self.db = self.client["DataBase-B"]
        self.collection  = self.db["ActiveEvents-B"]

    async def run(self, bookmakerId:int,  bookmakerName:str ) -> None:
        """
        bookmakerId: int :> bookmaker id
        bookmakerName: string :> bookmaker name
        """

        filtered_documents =  await self.collection.find(
            {
                "bookmakerName" : bookmakerName,
                "bookmakerId" : bookmakerId
                
            }
        ).to_list(10000)
            

        mapping_collection = self.client['OddSandMore']["Mapping"]

        await mapping_collection.insert_many(
            [
                document
                for document in filtered_documents
            ]
        )




if __name__ == "__main__":
    from asyncio import run
    app = Application(
        host="mongodb://localhost:27017",
        username="admin",
        password="admin"
    )

    run(app.run(
        bookmakerId=31,
        bookmakerName="sisal"
    ))
