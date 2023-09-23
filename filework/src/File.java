class File {
    private String fileName;
    private int fileSize;
    private String creationDate;
    private int accessCount;

    public File(String fileName, int fileSize, String creationDate, int accessCount) {
        this.fileName = fileName;
        this.fileSize = fileSize;
        this.creationDate = creationDate;
        this.accessCount = accessCount;
    }

    public String getFileName() {
        return fileName;
    }

    public void setFileName(String fileName) {
        this.fileName = fileName;
    }

    public int getFileSize() {
        return fileSize;
    }

    public void setFileSize(int fileSize) {
        this.fileSize = fileSize;
    }

    public String getCreationDate() {
        return creationDate;
    }

    public void setCreationDate(String creationDate) {
        this.creationDate = creationDate;
    }

    public int getAccessCount() {
        return accessCount;
    }

    public void setAccessCount(int accessCount) {
        this.accessCount = accessCount;
    }

    @Override
    public String toString() {
        return "Файл: " + fileName + ", Розмір: " + fileSize + ", Дата створення: " + creationDate + ", Кількість звернень: " + accessCount;
    }
}
