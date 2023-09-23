import java.util.Arrays;

public class Main {
    public static void main(String[] args) {
        File[] files = new File[3];
        files[0] = new File("file1.txt", 100, "2023-09-20", 5);
        files[1] = new File("file2.txt", 200, "2023-09-21", 8);
        files[2] = new File("file3.txt", 150, "2023-09-22", 3);

        Arrays.sort(files, (f1, f2) -> f1.getFileName().compareTo(f2.getFileName()));

        System.out.println("Список файлів в алфавітному порядку:");
        for (File file : files) {
            System.out.println(file);
        }

        int maxSize = 150;
        System.out.println("\nСписок файлів, розмір яких перевищує " + maxSize + ":");
        for (File file : files) {
            if (file.getFileSize() > maxSize) {
                System.out.println(file);
            }
        }

        int minAccessCount = 5;
        System.out.println("\nСписок файлів з кількістю звернень більше ніж " + minAccessCount + ":");
        for (File file : files) {
            if (file.getAccessCount() > minAccessCount) {
                System.out.println(file);
            }
        }
    }
}
