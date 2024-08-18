from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from PIL import Image
import os
from io import BytesIO

image_router = APIRouter()

BASE_UPLOAD_DIRECTORY = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "image"))

def get_directory(type: str):
    directory_mapping = {
        "user": os.path.join(BASE_UPLOAD_DIRECTORY, "users"),
        "job": os.path.join(BASE_UPLOAD_DIRECTORY, "jobs"),
        "submit": os.path.join(BASE_UPLOAD_DIRECTORY, "submits")
    }
    
    if type in directory_mapping:
        directory = directory_mapping[type]
        if not os.path.exists(directory):
            os.makedirs(directory)
        return directory
    else:
        raise HTTPException(status_code=404, detail="No type found or wrong type")

@image_router.post("/upload/{type}/{filename}")
async def upload_image(
    type: str,
    filename: str,
    file: UploadFile = File(...),
):
    directory = get_directory(type)
    width, height = 300, 300
    
    try:
        file_ext = os.path.splitext(file.filename)[1]
        file_location = os.path.join(directory, f"{filename}{file_ext}")
        
        # 로그 출력
        print(f"Saving file to: {file_location}")
        
        if os.path.exists(file_location):
            os.remove(file_location)
        
        image = Image.open(BytesIO(await file.read()))
        image = image.resize((width, height))
        image.save(file_location)

        return {"file_path": file_location}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Image processing error: {str(e)}")

@image_router.get("/view/{type}/{filename}")
async def view_image(type: str ,filename: str):
    directory = get_directory(type)
    
    # 파일 확장자 자동 추가
    possible_extensions = ['.png', '.jpg', '.jpeg', '.gif']
    
    # 파일이 확장자가 없을 경우, 각 확장자로 파일을 찾아봄
    for ext in possible_extensions:
        file_path = os.path.join(directory, f"{filename}{ext}")
        if os.path.exists(file_path):
            image = Image.open(file_path)
            img_byte_arr = BytesIO()
            image.save(img_byte_arr, format=image.format)
            img_byte_arr.seek(0)
            return StreamingResponse(img_byte_arr, media_type=f"image/{image.format.lower()}")
    
    # 파일을 찾지 못한 경우
    raise HTTPException(status_code=404, detail="File not found")
