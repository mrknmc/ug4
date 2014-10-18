-- Informatics 1 - Functional Programming
-- Tutorial 3
--
-- Week 5 - Due: 16/17 Oct.

import Data.Char
import Test.QuickCheck



-- 1. Map
-- a.
uppers :: String -> String
uppers = map toUpper

-- b.
doubles :: [Int] -> [Int]
doubles = map ((*) 2)

-- c.
penceToPounds :: [Int] -> [Float]
penceToPounds xs = map (divi 100) xs
    where divi a b = (fromIntegral b) / a

-- d.
uppers' :: String -> String
uppers' xs = [toUpper x | x <- xs]

prop_uppers :: String -> Bool
prop_uppers xs = uppers xs == uppers' xs



-- 2. Filter
-- a.
alphas :: String -> String
alphas = filter (isAlpha)

-- b.
rmChar ::  Char -> String -> String
rmChar c = filter (/= c)

-- c.
above :: Int -> [Int] -> [Int]
above i = filter (> i)

-- d.
unequals :: [(Int,Int)] -> [(Int,Int)]
unequals = (filter (uncurry (/=)))

-- e.
rmCharComp :: Char -> String -> String
rmCharComp c s = [c' | c' <- s, c /= c']

prop_rmChar :: Char -> String -> Bool
prop_rmChar c s = rmChar c s == rmCharComp c s



-- 3. Comprehensions vs. map & filter
-- a.
upperChars :: String -> String
upperChars s = [toUpper c | c <- s, isAlpha c]

upperChars' :: String -> String
upperChars' s = map toUpper (filter isAlpha s)

prop_upperChars :: String -> Bool
prop_upperChars s = upperChars s == upperChars' s

-- b.
largeDoubles :: [Int] -> [Int]
largeDoubles xs = [2 * x | x <- xs, x > 3]

largeDoubles' :: [Int] -> [Int]
largeDoubles' xs = map (* 2) (filter (> 3) xs)

prop_largeDoubles :: [Int] -> Bool
prop_largeDoubles xs = largeDoubles xs == largeDoubles' xs

-- c.
reverseEven :: [String] -> [String]
reverseEven strs = [reverse s | s <- strs, even (length s)]

reverseEven' :: [String] -> [String]
reverseEven' s = map reverse (filter (even . length) s)

prop_reverseEven :: [String] -> Bool
prop_reverseEven strs = reverseEven strs == reverseEven' strs



-- 4. Foldr
-- a.
productRec :: [Int] -> Int
productRec []     = 1
productRec (x:xs) = x * productRec xs

productFold :: [Int] -> Int
productFold xs = foldr (*) 1 xs

prop_product :: [Int] -> Bool
prop_product xs = productRec xs == productFold xs

-- b.
andRec :: [Bool] -> Bool
andRec [] = True
andRec (x:xs) = x && andRec xs

andFold :: [Bool] -> Bool
andFold xs = foldr (&&) True xs

prop_and :: [Bool] -> Bool
prop_and xs = andRec xs == andFold xs

-- c.
concatRec :: [[a]] -> [a]
concatRec [] = []
concatRec (x:xs) = x ++ concatRec xs

concatFold :: [[a]] -> [a]
concatFold xs = foldr (++) [] xs

prop_concat :: [String] -> Bool
prop_concat strs = concatRec strs == concatFold strs

-- d.
rmCharsRec :: String -> String -> String
rmCharsRec [] str = str
rmCharsRec (c:chars) str = rmChar c (rmCharsRec chars str)
--rmCharsRec (c:chars) str = rmChar c str ++ rmCharsRec chars str

rmCharsFold :: String -> String -> String
rmCharsFold chars str = foldr rmChar str chars

prop_rmChars :: String -> String -> Bool
prop_rmChars chars str = rmCharsRec chars str == rmCharsFold chars str



type Matrix = [[Int]]


-- 5
-- a.
uniform :: [Int] -> Bool
uniform [] = True
uniform (x:xs) = all (== x) xs

-- b.
valid :: Matrix -> Bool
valid m = uniform (map length m) && m /= [] && m /= [[]]

-- 6.

zipWith' f xs ys = [f x y | (x,y) <- zip xs ys]

zipWith'' f xs ys = map (uncurry f) (zip xs ys)

-- 7.
plusM :: Matrix -> Matrix -> Matrix
plusM m1 m2
  | valid m1 &&
    valid m2 &&
    length m1 == length m2 &&
    length (head m1) == length (head m2) = zipWith plusRow m1 m2
  | otherwise = error "Not valid matrices."

plusRow :: [Int] -> [Int] -> [Int]
plusRow xs ys = map (uncurry (+)) (zip xs ys)

-- 8.
timesM :: Matrix -> Matrix -> Matrix
timesM m1 m2
  | valid m1 &&
    valid m2 &&
    length (head m1) == length m2 = [ [ timesRow row col | col <- transpose m2 ] | row <- m1 ]
  | otherwise = error "Lol, no."

timesRow :: [Int] -> [Int] -> Int
timesRow xs ys = sum (map (uncurry (*)) (zip xs ys))

-- Optional material
-- 9.
