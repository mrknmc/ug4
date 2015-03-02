# RE: Distributed Software Development, and why I don't like it.

I enjoyed reading your article and given your experience I can see why you don't like DSD. However, in this response I would like to touch on some things that I believe might not necessarily have been the fault of DSD.

Firstly, your comments on team spirit resonated with me and as someone who is fairly open to DSD I agree that this is one of its disadvantages. I believe, however, that if your "local" team is large enough or you work in an office-share this can be helped. Additionally, I think it is fair to say that remote working is not for everyone.

Secondly, there is the language barrier problem. I think this is a really big lapse in judgement by the management of the company. I understand that the team was spread across the globe but if your management cannot ensure that you all develop in the same language then maybe they should have enforced regular code reviews (which I would advocate for anyway).

The reason why I claim that is because I was part of a  DSD team and we didn't have that problem at all. I worked at a company where some of the work for our main library was outsourced to a consultancy in Russia (the company could not scale quickly enough). The management set clear coding standards and the developers from Russia had to develop code in English (including comments). Moreover, they went through a testing period where my team would review their code and sign off on it.

Thirdly, I think that SLOC is a terrible metric. Period. It promotes bad practices such as copy-pasting code, avoiding re-factoring, and disadvantages people who write clean code. Additionally, developers could start optimising for SLOC and that could lead to unneeded complexity [ref]. Instead of measuring SLOC why not use some bug tracking or project management software e.g. Trello, Fogbugz, or Jira. 

I believe the way they tracked work at the company I worked for was by daily stand-up meetings and going trough comments on cases that we were supposed to update regularly. I would imagine this takes up more time than counting SLOC but gives you a better idea of how much work people did.

> Was it fair? Was the developer really intentionally slacking? Who knows.

I feel that since you say "who knows" it is a little bit unfair to use it as part of your argument. There could have been valid reasons for that person being fired and I think it's a little bit unfair to suggest otherwise unless you know for sure.

Finally, I think that having your (project) manager start working 8 hours after you is less then ideal. There are limits to how distributed your team should be and I think there should definitely be a larger time overlap between you and your supervisor. Otherwise the communication will become the bottleneck.

http://en.wikipedia.org/wiki/Source_lines_of_code#Disadvantages
