-- Informatics 1 - Functional Programming 
-- Tutorial 1
--
-- Due: the tutorial of week 3 (2/3 Oct.)

import Data.Char
import Data.List
import Test.QuickCheck



-- 1. halveEvens

-- List-comprehension version
halveEvens :: [Int] -> [Int]
halveEvens xs = [x `div` 2 | x <- xs, even x] 

-- Recursive version
halveEvensRec :: [Int] -> [Int]
halveEvensRec [] = []
halveEvensRec (x:xs)
  | even x = x `div` 2 : halveEvensRec xs
  | otherwise = halveEvensRec xs 

-- Mutual test
prop_halveEvens :: [Int] -> Bool
prop_halveEvens xs = halveEvens xs == halveEvensRec xs



-- 2. inRange

-- List-comprehension version
inRange :: Int -> Int -> [Int] -> [Int]
inRange lo hi xs = [x | x <- xs, x >= lo, x <= hi] 

-- Recursive version
inRangeRec :: Int -> Int -> [Int] -> [Int]
inRangeRec _ _ [] = []
inRangeRec lo hi (x:xs)
  | x >= lo && x <= hi = x : inRangeRec lo hi xs
  | otherwise = inRangeRec lo hi xs

-- Mutual test
prop_inRange :: Int -> Int -> [Int] -> Bool
prop_inRange lo hi xs = inRange lo hi xs == inRangeRec lo hi xs 



-- 3. sumPositives: sum up all the positive numbers in a list

-- List-comprehension version
countPositives :: [Int] -> Int
countPositives xs = length [x | x <- xs, x > 0] 

-- Recursive version
countPositivesRec :: [Int] -> Int
countPositivesRec [] = 0
countPositivesRec (x:xs)
  | x > 0 = 1 + countPositivesRec xs
  | otherwise = countPositivesRec xs

-- Mutual test
prop_countPositives :: [Int] -> Bool
prop_countPositives xs = countPositives xs == countPositivesRec xs



-- 4. pennypincher

-- Helper function
discount :: Int -> Int
discount p = round (0.9 * fromIntegral p)

-- List-comprehension version
pennypincher :: [Int] -> Int
pennypincher ps = sum [discount p | p <- ps, discount p <= 19900]

-- Recursive version
pennypincherRec :: [Int] -> Int
pennypincherRec [] = 0
pennypincherRec (p:ps)
  | discount p <= 19900 = discount p + pennypincherRec ps
  | otherwise = pennypincherRec ps

-- Mutual test
prop_pennypincher :: [Int] -> Bool
prop_pennypincher ps = pennypincher ps == pennypincherRec ps 



-- 5. sumDigits

-- List-comprehension version
multDigits :: String -> Int
multDigits xs = product [digitToInt x | x <- xs, isDigit x]

-- Recursive version
multDigitsRec :: String -> Int
multDigitsRec "" = 1
multDigitsRec (x:xs)
  | isDigit x = digitToInt x * multDigitsRec xs
  | otherwise = multDigitsRec xs

-- Mutual test
prop_multDigits :: String -> Bool
prop_multDigits xs = multDigits xs == multDigitsRec xs



-- 6. capitalise

-- List-comprehension version
capitalise :: String -> String
capitalise xs = [(if i == 0 then toUpper else toLower) x | (i, x) <- zip [0..] xs]

-- Recursive version
capitaliseRec :: String -> String
capitaliseRec [] = []
capitaliseRec [x] = [toUpper x]
capitaliseRec (xs) = capitaliseRec (init xs) ++ [toLower (last xs)]

-- Mutual test
prop_capitalise :: String -> Bool
prop_capitalise xs = capitalise xs == capitaliseRec xs



-- 7. title

-- List-comprehension version
title :: [String] -> [String]
title ss = [if i == 0 then capitalise s else if length s < 4 then [toLower c | c <- s] else capitalise s | (i, s) <- zip [0..] ss]

-- Recursive version
titleRec :: [String] -> [String]
titleRec [] = []
titleRec [s] = [capitalise s]
titleRec ss
  | length l < 4 = titleRec (init ss) ++ [[toLower c | c <- l]]
  | otherwise = titleRec (init ss) ++ [capitalise l]
  where l = last ss

-- mutual test
prop_title :: [String] -> Bool
prop_title ss = title ss == titleRec ss 




-- Optional Material

-- 8. crosswordFind

-- List-comprehension version
crosswordFind :: Char -> Int -> Int -> [String] -> [String]
crosswordFind = undefined

-- Recursive version
crosswordFindRec :: Char -> Int -> Int -> [String] -> [String]
crosswordFindRec = undefined

-- Mutual test
prop_crosswordFind :: Char -> Int -> Int -> [String] -> Bool
prop_crosswordFind = undefined 



-- 9. search

-- List-comprehension version

search :: String -> Char -> [Int]
search = undefined

-- Recursive version
searchRec :: String -> Char -> [Int]
searchRec = undefined

-- Mutual test
prop_search :: String -> Char -> Bool
prop_search = undefined


-- 10. contains

-- List-comprehension version
contains :: String -> String -> Bool
contains = undefined

-- Recursive version
containsRec :: String -> String -> Bool
containsRec = undefined

-- Mutual test
prop_contains :: String -> String -> Bool
prop_contains = undefined

