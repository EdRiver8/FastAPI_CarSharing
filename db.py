from sqlmodel import create_engine, Session

# engine, representa la conexion con la db
engine = create_engine(
  "sqlite:///carsharing.db", # string de conexion
  connect_args={"check_same_thread": False}, # necesario para SQLite
  echo=True # Log generated SQL y los muestra por consola
)

# sirve como inyeccion de dependencias
def get_session():
  with Session(engine) as session:
    # yield es como usar un bloque 'with', si existe una excepcion no se guardara nada
    yield session # funcion generadora, da proteccion de rollback en caso que algo salga mal