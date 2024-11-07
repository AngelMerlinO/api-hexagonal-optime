from fastapi import FastAPI, Request, HTTPException
import httpx

app = FastAPI()

async def forward_request(request: Request, base_url: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(
                method=request.method,
                url=f"{base_url}{request.url.path}",
                headers=request.headers,
                params=request.query_params,
                content=await request.body(),
            )
            response.raise_for_status() 
            return response.json() 
        except httpx.HTTPStatusError as e:
            print(f"Error en la solicitud al servidor: {e}")
            raise HTTPException(status_code=e.response.status_code, detail=f"Error en el servidor: {e}")
        except httpx.RequestError as e:
            print(f"Error de conexión con el servidor: {e}")
            raise HTTPException(status_code=503, detail="El servicio no está disponible")
    
## Rutas para usuarios
@app.api_route("/api/v1/users/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def users_service(request: Request, path: str):
    try:
        response = await forward_request(request, "http://localhost:8001")
        print("Contenido de response:", response)  
        return response
    except Exception as e:
        print(f"Error procesando la solicitud: {e}")
        raise HTTPException(status_code=500, detail=str(e))


## Rutas para contactos
@app.api_route("/api/v1/contacts/{path:path}", methods=["POST"])
async def contacts_service(request: Request, path: str):
    try:
        response = await forward_request(request, "http://localhost:8002")
        print("Contenido de response:", response)  
        return response
    except Exception as e:
        print(f"Error procesando la solicitud: {e}")
        raise HTTPException(status_code=500, detail=str(e))