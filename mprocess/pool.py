import multiprocessing as mp 

def selfSquared(anumber):
    print(mp.current_process().name,':: number =', anumber)
    return (anumber*anumber)

if __name__ == '__main__':
    print ('cpucount =',mp.cpu_count())
    numberSequence = [31,53,79]
    pool = mp.Pool(processes=3)

    print(mp.current_process().name,'::',pool.map(selfSquared,numberSequence))