-- Informatics 1 - Functional Programming
-- Tutorial 4
--
-- Due: the tutorial of week 6 (23/24 Oct)

import Data.List (nub)
import Data.Char
import Test.QuickCheck
import Network.HTTP (simpleHTTP,getRequest,getResponseBody)

-- <type decls>

type Link = String
type Name = String
type Email = String
type HTML = String
type URL = String

-- </type decls>
-- <sample data>

testURL     = "http://www.inf.ed.ac.uk/teaching/courses/inf1/fp/testpage.html"

testHTML :: String
testHTML =    "<html>"
           ++ "<head>"
           ++ "<title>FP: Tutorial 4</title>"
           ++ "</head>"
           ++ "<body>"
           ++ "<h1>A Boring test page</h1>"
           ++ "<h2>for tutorial 4</h2>"
           ++ "<a href=\"http://www.inf.ed.ac.uk/teaching/courses/inf1/fp/\">FP Website</a><br>"
           ++ "<b>Lecturer:</b> <a href=\"mailto:dts@inf.ed.ac.uk\">Don Sannella</a><br>"
           ++ "<b>TA:</b> <a href=\"mailto:m.k.lehtinen@sms.ed.ac.uk\">Karoliina Lehtinen</a>"
           ++ "</body>"
           ++ "</html>"

testLinks :: [Link]
testLinks = [ "http://www.inf.ed.ac.uk/teaching/courses/inf1/fp/\">FP Website</a><br><b>Lecturer:</b> "
            , "mailto:dts@inf.ed.ac.uk\">Don Sannella</a><br><b>TA:</b> "
            , "mailto:m.k.lehtinen@sms.ed.ac.uk\">Karoliina Lehtinen</a></body></html>" ]


testAddrBook :: [(Name,Email)]
testAddrBook = [ ("Don Sannella","dts@inf.ed.ac.uk")
               , ("Karoliina Lehtinen","m.k.lehtinen@sms.ed.ac.uk")]

-- </sample data>
-- <system interaction>

getURL :: String -> IO String
getURL url = simpleHTTP (getRequest url) >>= getResponseBody

emailsFromURL :: URL -> IO ()
emailsFromURL url =
  do html <- getURL url
     let emails = (emailsFromHTML html)
     putStr (ppAddrBook emails)

emailsByNameFromURL :: URL -> Name -> IO ()
emailsByNameFromURL url name =
  do html <- getURL url
     let emails = (emailsByNameFromHTML html name)
     putStr (ppAddrBook emails)

-- </system interaction>
-- <exercises>

-- 1.
sameString :: String -> String -> Bool
sameString s1 s2 = map toUpper s1 == map toUpper s2


-- 2.
prefix :: String -> String -> Bool
prefix substr str = substr `sameString` take (length substr) str

prop_prefix :: String -> Int -> Bool
prop_prefix str n  =  prefix substr (map toLower str) &&
		      prefix substr (map toUpper str)
                          where
                            substr  =  take n str


-- 3.
contains :: String -> String -> Bool
contains str substr = or [prefix substr (drop n str) | n <- [0..length str - 1]]

prop_contains :: String -> Int -> Int -> Bool
prop_contains str i j = contains (map toLower str) substr &&
          contains (map toUpper str) substr
                          where substr = take i (drop j str)


-- 4.
takeUntil :: String -> String -> String
takeUntil _ [] = []
takeUntil substr (c:str)
  | prefix substr (c:str) = []
  | otherwise = c : takeUntil substr str

dropUntil :: String -> String -> String
dropUntil _ [] = []
dropUntil substr str
  | prefix substr str = drop (length substr) str
  | otherwise = dropUntil substr (tail str)


-- 5.
split :: String -> String -> [String]
split "" str  = error "Can't split on an empty string"
split sep str
    | str `contains` sep = takeUntil sep str : split sep (dropUntil sep str)
    | otherwise        = [str]

reconstruct :: String -> [String] -> String
reconstruct _ [] = []
reconstruct _ [str] = str
reconstruct sep (str:strs) = str ++ sep ++ reconstruct sep strs

prop_split :: Char -> String -> String -> Bool
prop_split c sep str = reconstruct sep' (split sep' str) `sameString` str
  where sep' = c : sep

-- 6.
linksFromHTML :: HTML -> [Link]
linksFromHTML doc = tail (split "<a href=\"" doc)

testLinksFromHTML :: Bool
testLinksFromHTML  =  linksFromHTML testHTML == testLinks


-- 7.
takeEmails :: [Link] -> [Link]
takeEmails links = [ link | link <- links, prefix "mailto:" link]


-- 8.
link2pair :: Link -> (Name, Email)
link2pair link = (head (tail l), head l)
    where l = split "\">" (head (split "</a>" link))


-- 9.
emailsFromHTML :: HTML -> [(Name,Email)]
emailsFromHTML doc = nub (map link2pair (takeEmails (linksFromHTML doc)))

testEmailsFromHTML :: Bool
testEmailsFromHTML  =  emailsFromHTML testHTML == testAddrBook


-- 10.
findEmail :: Name -> [(Name, Email)] -> [(Name, Email)]
findEmail name book = [ (n, e) | (n, e) <- book, contains n name]


-- 11.
emailsByNameFromHTML :: HTML -> Name -> [(Name,Email)]
emailsByNameFromHTML name doc = findEmail name (emailsFromHTML doc)


-- Optional Material

-- 12.
ppAddrBook :: [(Name, Email)] -> String
ppAddrBook addr = unlines [ name ++ ": " ++ email | (name,email) <- addr ]
