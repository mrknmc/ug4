-- Informatics 1 - Functional Programming
-- Tutorial 2
--
-- Week 4 - due: 9/10 Oct.

import Data.Char
import Data.List
import Test.QuickCheck


-- 1.
rotate :: Int -> [Char] -> [Char]
rotate n str
  | n < 0 = error "n is negative"
  | n > length str = error "n too large"
  | otherwise = drop n str ++ take n str

-- 2.
prop_rotate :: Int -> String -> Bool
prop_rotate k str = rotate (l - m) (rotate m str) == str
                        where l = length str
                              m = if l == 0 then 0 else k `mod` l

-- 3.
makeKey :: Int -> [(Char, Char)]
makeKey k = zip ['A'..'Z'] (rotate k ['A'..'Z'])

-- 4.
lookUp :: Char -> [(Char, Char)] -> Char
lookUp c xs = head ([ y | (x, y) <- xs, x == c] ++ [c])

lookUpRec :: Char -> [(Char, Char)] -> Char
lookUpRec c [] = c
lookUpRec c ((key,val):rest)
  | key == c = val
  | otherwise = lookUpRec c rest

prop_lookUp :: Char -> [(Char, Char)] -> Bool
prop_lookUp c xs = lookUp c xs == lookUpRec c xs

-- 5.
encipher :: Int -> Char -> Char
encipher i c = lookUp c (makeKey i)

-- 6.
normalize :: String -> String
normalize [] = []
normalize (c:s)
  | isDigit c || isAlpha c = toUpper c : normalize s
  | otherwise = normalize s

-- 7.
encipherStr :: Int -> String -> String
encipherStr k s = [encipher k c | c <- (normalize s)]

-- 8.
reverseKey :: [(Char, Char)] -> [(Char, Char)]
reverseKey zs = [(y, x) | (x, y) <- zs]

reverseKeyRec :: [(Char, Char)] -> [(Char, Char)]
reverseKeyRec [] = []
reverseKeyRec ((k, v) : rest) = (v, k) : reverseKeyRec rest

prop_reverseKey :: [(Char, Char)] -> Bool
prop_reverseKey s = reverseKey s == reverseKeyRec s

-- 9.
decipher :: Int -> Char -> Char
decipher k c = lookUp c (reverseKey (makeKey k))

decipherStr :: Int -> String -> String
decipherStr k s = [lookUp c rev | c <- s]
  where rev = reverseKey (makeKey k)

-- 10.
contains :: String -> String -> Bool
contains _ [] = True
contains [] _ = False
contains s1 s2 = isPrefixOf s2 s1 || contains (tail s1) s2

-- 11.
candidates :: String -> [(Int, String)]
candidates s = undefined



-- Optional Material

-- 12.
splitEachFive :: String -> [String]
splitEachFive = undefined

-- 13.
prop_transpose :: String -> Bool
prop_transpose = undefined

-- 14.
encrypt :: Int -> String -> String
encrypt = undefined

-- 15.
decrypt :: Int -> String -> String
decrypt = undefined

-- Challenge (Optional)

-- 16.
countFreqs :: String -> [(Char, Int)]
countFreqs = undefined

-- 17
freqDecipher :: String -> [String]
freqDecipher = undefined
