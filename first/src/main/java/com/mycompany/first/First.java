/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 */

package com.mycompany.first;
import java.util.Scanner;
import java.util.Random;
/**
 *
 * @author Sinan
 */
public class First {

    public static void main(String[] args) {
        
        
        int[] array = new int[5];  // Create an array of size 5
        Random rand = new Random();  // Create an instance of the Random class

        // Fill the array with randomly generated integers
        for (int i = 0; i < array.length; i++) {
            array[i] = rand.nextInt(100);  // Generate a random integer between 0 and 99
        }

        // Print the elements of the array
        System.out.println("The elements of the array are:");
        for (int i = 0; i < array.length; i++) {
            System.out.println(array[i]);
        }
       
    }
    
}
