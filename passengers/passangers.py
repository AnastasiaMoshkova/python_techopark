# -*- encoding: utf-8 -*-


def process(data, events, car):

    j=0
    for event in events:
        if event['type']=='walk':
            for train in data:
                for carT in train['cars']:
                    for people in carT['people']:
                        if people==event['passenger']:
                            carT['people'].remove(people)
                            number=0
                            number=train['cars'].index(carT)+int(event['distance'])
                            if number<0:return -1
                            train['cars'][number]['people'].append(people)
                            break
                    else:
                        continue
                    break
                else:
                    continue
                break
            else:
                continue

        if event['type']=='switch':
            for train in data:
                if train['name']==event['train_from']:
                    train_ch=[]
                    i=0
                    for i in range(int(event['cars'])):
                        if not train['cars']:return -1
                        train_ch.append(train['cars'].pop())
                        train_ch.reverse()
                    for train in data:
                        if train['name']==event['train_to']:
                           train['cars'].extend(train_ch)
                           break
                           break
                    else:
                        continue
                        continue
                    break
            else:
                continue

    for train in data:
        for carQ in train['cars']:
            if carQ['name']==car:
                for people in carQ['people']:
                    j=j+1
             
    
    return j
