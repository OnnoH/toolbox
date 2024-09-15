import java.util.Random;

class RandomCity {

    public static void main(String[] args) {
        String[] cities = {"New York", "London", "Paris", "Munich", "Tokio", "Sydney", "Amsterdam"};
        System.out.println(getRandomCity(cities));
    }

    private static String getRandomCity(String[] array) {
        int rnd = new Random().nextInt(array.length);
        return array[rnd];
    }
}