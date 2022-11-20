import os
import shutil
import sys
from PIL import Image
import discord



# Variables
svc_table = {
	"0x1": "Result ControlMemory(u32* outaddr, u32 addr0, u32 addr1, u32 size, u32 operation, u32 permissions) (outaddr is usually the same as the input addr0)",
	"0x2": "Result QueryMemory(MemoryInfo* info, PageInfo* out, u32 Addr)",
	"0x3": "void ExitProcess(void)",
	"0x4": "Result GetProcessAffinityMask(u8* affinitymask, Handle process, s32 processorcount)",
	"0x5": "Result SetProcessAffinityMask(Handle process, u8* affinitymask, s32 processorcount)",
	"0x6": "Result GetProcessIdealProcessor(s32 *idealprocessor, Handle process)",
	"0x7": "Result SetProcessIdealProcessor(Handle process, s32 idealprocessor)",
	"0x8": "Result CreateThread(Handle* thread, func entrypoint, u32 arg, u32 stacktop, s32 threadpriority, s32 processorid)",
	"0x9": "void ExitThread(void)",
	"0xA": "void SleepThread(s64 nanoseconds)",
	"0xB": "Result GetThreadPriority(s32* priority, Handle thread)",
	"0xC": "Result SetThreadPriority(Handle thread, s32 priority)",
	"0xD": "Result GetThreadAffinityMask(u8* affinitymask, Handle thread, s32 processorcount)",
	"0xE": "Result SetThreadAffinityMask(Handle thread, u8* affinitymask, s32 processorcount)",
	"0xF": "Result GetThreadIdealProcessor(s32* processorid, Handle thread)",
	"0x10": "Result SetThreadIdealProcessor(Handle thread, s32 processorid)",
	"0x11": "s32 GetCurrentProcessorNumber(void)",
	"0x12": "Result Run(Handle process, StartupInfo* info) (This starts the main() thread. Buf+0 is main-thread priority, Buf+4 is main-thread stack-size.)",
	"0x13": "Result CreateMutex(Handle* mutex, bool initialLocked)",
	"0x14": "Result ReleaseMutex(Handle mutex)",
	"0x15": "Result CreateSemaphore(Handle* semaphore, s32 initialCount, s32 maxCount)",
	"0x16": "Result ReleaseSemaphore(s32* count, Handle semaphore, s32 releaseCount)",
	"0x17": "Result CreateEvent(Handle* event, ResetType resettype)",
	"0x18": "Result SignalEvent(Handle event)",
	"0x19": "Result ClearEvent(Handle event)",
	"0x1A": "Result CreateTimer(Handle* timer, ResetType resettype)",
	"0x1B": "Result SetTimer(Handle timer, s64 initial, s64 interval)",
	"0x1C": "Result CancelTimer(Handle timer)",
	"0x1D": "Result ClearTimer(Handle timer)",
	"0x1E": "Result CreateMemoryBlock(Handle* memblock, u32 memory, u32 size, u32 mypermission, u32 otherpermission)",
	"0x1F": "Result MapMemoryBlock(Handle memblock, u32 addr, u32 mypermissions, u32 otherpermission)",
	"0x20": "Result UnmapMemoryBlock(Handle memblock, u32 addr)",
	"0x21": "Result CreateAddressArbiter(Handle* arbiter)",
	"0x22": "Result ArbitrateAddress(Handle arbiter, u32 addr, ArbitrationType type, s32 value)",
	"0x23": "Result CloseHandle(Handle handle)",
	"0x24": "Result WaitSynchronization1(Handle handle, s64 nanoseconds)",
	"0x25": "Result WaitSynchronizationN(s32* out, Handle* handles, s32 handlecount, bool waitAll, s64 nanoseconds)",
	"0x26": "Result SignalAndWait(s32* out, Handle signal, Handle* handles, s32 handleCount, bool waitAll, s64 nanoseconds)",
	"0x27": "Result DuplicateHandle(Handle* out, Handle original)",
	"0x28": "s64 GetSystemTick(void)",
	"0x29": "Result GetHandleInfo(s64* out, Handle handle, HandleInfoType type)",
	"0x2A": "Result GetSystemInfo(s64* out, SystemInfoType type, s32 param)",
	"0x2B": "Result GetProcessInfo(s64* out, Handle process, ProcessInfoType type)",
	"0x2C": "Result GetThreadInfo(s64* out, Handle thread, ThreadInfoType type)",
	"0x2D": "Result ConnectToPort(Handle* out, const char* portName)",
	"0x2E": "Result SendSyncRequest1(Handle session) (Stubbed)",
	"0x2F": "Result SendSyncRequest2(Handle session) (Stubbed)",
	"0x30": "Result SendSyncRequest3(Handle session) (Stubbed)",
	"0x31": "Result SendSyncRequest4(Handle session) (Stubbed)",
	"0x32": "Result SendSyncRequest(Handle session)",
	"0x33": "Result OpenProcess(Handle* process, u32 processId)",
	"0x34": "Result OpenThread(Handle* thread, Handle process, u32 threadId)",
	"0x35": "Result GetProcessId(u32* processId, Handle process)",
	"0x36": "Result GetProcessIdOfThread(u32* processId, Handle thread)",
	"0x37": "Result GetThreadId(u32* threadId, Handle thread)",
	"0x38": "Result GetResourceLimit(Handle* resourceLimit, Handle process)",
	"0x39": "Result GetResourceLimitLimitValues(s64* values, Handle resourceLimit, LimitableResource* names, s32 nameCount)",
	"0x3A": "Result GetResourceLimitCurrentValues(s64* values, Handle resourceLimit, LimitableResource* names, s32 nameCount)",
	"0x3B": "Result GetThreadContext(ThreadContext* context, Handle thread) (Stubbed)",
	"0x3C": "Break(BreakReason)",
	"0x3D": "OutputDebugString(void const, int) (Does nothing on non-debug units)",
	"0x3E": "ControlPerformanceCounter(unsigned long long, int, unsigned int, unsigned long long)",
	"0x47": "Result CreatePort(Handle* portServer, Handle* portClient, const char* name, s32 maxSessions)",
	"0x48": "Result CreateSessionToPort(Handle* session, Handle port)",
	"0x49": "Result CreateSession(Handle* sessionServer, Handle* sessionClient)",
	"0x4A": "Result AcceptSession(Handle* session, Handle port)",
	"0x4B": "Result ReplyAndReceive1(s32* index, Handle* handles, s32 handleCount, Handle replyTarget) (Stubbed)",
	"0x4C": "Result ReplyAndReceive2(s32* index, Handle* handles, s32 handleCount, Handle replyTarget) (Stubbed)",
	"0x4D": "Result ReplyAndReceive3(s32* index, Handle* handles, s32 handleCount, Handle replyTarget) (Stubbed)",
	"0x4E": "Result ReplyAndReceive4(s32* index, Handle* handles, s32 handleCount, Handle replyTarget) (Stubbed)",
	"0x4F": "Result ReplyAndReceive(s32* index, Handle* handles, s32 handleCount, Handle replyTarget)",
	"0x50": "Result BindInterrupt(Interrupt name, Handle syncObject, s32 priority, bool isManualClear)",
	"0x51": "Result UnbindInterrupt(Interrupt name, Handle syncObject)",
	"0x52": "Result InvalidateProcessDataCache(Handle process, void* addr, u32 size)",
	"0x53": "Result StoreProcessDataCache(Handle process, void const* addr, u32 size)",
	"0x54": "Result FlushProcessDataCache(Handle process, void const* addr, u32 size)",
	"0x55": "Result StartInterProcessDma(Handle* dma, Handle dstProcess, void* dst, Handle srcProcess, const void* src, u32 size, const DmaConfig& config )",
	"0x56": "Result StopDma(Handle dma)",
	"0x57": "Result GetDmaState(DmaState* state, Handle dma)",
	"0x58": "RestartDma(nn::Handle, void *, void const*, unsigned int, signed char)",
	"0x60": "Result DebugActiveProcess(Handle* debug, u32 processID)",
	"0x61": "Result BreakDebugProcess(Handle debug)",
	"0x62": "Result TerminateDebugProcess(Handle debug)",
	"0x63": "Result GetProcessDebugEvent(DebugEventInfo* info, Handle debug)",
	"0x64": "Result ContinueDebugEvent(Handle debug, u32 flags)",
	"0x65": "Result GetProcessList(s32* processCount, u32* processIds, s32 processIdMaxCount)",
	"0x66": "Result GetThreadList(s32* threadCount, u32* threadIds, s32 threadIdMaxCount, Handle domain)",
	"0x67": "Result GetDebugThreadContext(ThreadContext* context, Handle debug, u32 threadId, u32 controlFlags)",
	"0x68": "Result SetDebugThreadContext(Handle debug, u32 threadId, ThreadContext* context, u32 controlFlags)",
	"0x69": "Result QueryDebugProcessMemory(MemoryInfo* blockInfo, PageInfo* pageInfo, Handle process, u32 addr)",
	"0x6A": "Result ReadProcessMemory(void* buffer, Handle debug, u32 addr, u32 size)",
	"0x6B": "Result WriteProcessMemory(Handle debug, void const* buffer, u32 addr, u32 size)",
	"0x6C": "Result SetHardwareBreakPoint(s32 registerId, u32 control, u32 value)",
	"0x6D": "GetDebugThreadParam(long long *, int *, nn::Handle, unsigned int, nn::dmnt::DebugThreadParam) (Disabled on regular kernel)",
	"0x70": "ControlProcessMemory(Handle KProcess, unsigned int Addr0, unsigned int Addr1, unsigned int Size, unsigned int Type, unsigned int Permissions)",
	"0x71": "MapProcessMemory(Handle KProcess, unsigned int StartAddr, unsigned int EndAddr)",
	"0x72": "UnmapProcessMemory(Handle KProcess, unsigned int StartAddr, unsigned int EndAddr)",
	"0x73": "?",
	"0x74": "Stubbed on regular kernel",
	"0x75": "?",
	"0x76": "TerminateProcess(Handle)",
	"0x77": "(Handle KProcess, Handle KResourceLimit)",
	"0x78": "CreateResourceLimit(Handle *KResourceLimit)",
	"0x79": "?",
	"0x7A": "DisableExecuteNever(unsigned int Addr, unsigned int Size) (Stubbed for regular kernel beginning with 2.0.0-2)",
	"0x7C": "KernelSetState(unsigned int Type, unsigned int Param0, unsigned int Param1, unsigned int Param2) (The Type determines the usage of each param)",
	"0x7D": "QueryProcessMemory(MemInfo *Info, unsigned int *Out, Handle KProcess, unsigned int Addr)",
	"0xFF": "Debug related (The Syscall access control mask doesn't apply for this SVC)"
}


help_messages = {
	"ja": """```
V.help [LANGUAGE]
  -> このメッセージを表示します (LANGUAGE: ja, en, fr)

V.about
  -> このBOTの情報を表示します

V.bg (画像ファイルを添付)
  -> 画像をCTRPFの背景で使用できる形式にサイズ変更、変換します

V.kcd [キーコード]
  -> [キーコード] をボタンに変換します ( 'V.kcd 3' => 'A + B' )

V.key [ボタン]
  -> [ボタン] をキーコードに変換します。( 'V.key A B' => '00000003' )

V.svc [ID]
  -> [ID] に対する3DSのSVCの詳細を返します ( 'V.svc 0x9' => 'void ExitThread(void)' )
```""", # ja


	"en": """```
V.help [LANGUAGE]
  -> Display this message (LANGUAGE: ja, en, fr)

V.about
  -> Display information about this BOT

V.bg (Attach image file)
  -> Resize and convert image to a format usable for CTRPF backgrounds

V.kcd [keycode].
  -> convert [keycode] to a button ( 'V.kcd 3' => 'A + B' )

V.key [button].
  -> convert [button] to keycode ( 'V.key A B' => '00000003' )

V.svc [ID]
  -> returns 3DS SVC details for [ID] ( 'V.svc 0x9' => 'void ExitThread(void)' )
```""", # en


	"fr": """```
V.help [LANGUAGE]
  -> Afficher ce message (LANGUE : ja, en, fr)

V.about
  -> Affiche des informations sur ce BOT

V.bg (joindre un fichier image)
  -> Redimensionne et convertit l'image dans un format utilisable pour les arrière-plans du CTRPF.

V.kcd [keycode].
  -> convertit [keycode] en bouton ('V.kcd 3' => 'A + B' )

V.key [button].
  -> convertit [bouton] en keycode ('V.key A B' => '00000003' )

V.svc [ID]
  -> renvoie les détails du SVC de 3DS pour [ID] ('V.svc 0x9' => 'void ExitThread(void)' )
```""", # fr
}
# End of Variables



# Functions
def key_to_str(keys):
	keys_text = ("A", "B", "Select", "Start", "Right", "Left", "Up", "Down", "R", "L", "X", "Y", "", "", "ZL", "ZR", "", "", "", "", "Touch", "", "", "", "SR", "SL", "SU", "SD", "CR", "CL", "CU", "CD")
	ret = ""
	plus = False

	for i in range(32):
		if (keys & (1 << i)):
			key = keys_text[i]
			if not key: continue
			if plus: ret += " + "
			ret += key
			plus = True

	return ret


def button_to_code(buttons):
	buttons = " ".join(list(set([i.casefold() for i in buttons.split(" ")])))
	ret = 0
	button_codes = (0x80000000, 0x40000000, 0x20000000, 0x10000000, 0x8000000, 0x4000000, 0x2000000, 0x1000000, 0x100000, 0x8000, 0x4000, 0x800, 0x400, 0x200, 0x100, 0x80, 0x40, 0x20, 0x10, 0x8, 0x4, 0x2, 0x1, 0x80000000, 0x40000000, 0x20000000, 0x10000000, 0x8000000, 0x4000000, 0x2000000, 0x1000000, 0x80, 0x40, 0x20, 0x10, 0x80, 0x40, 0x20, 0x10)
	button_names = ("cd", "cu", "cl", "cr", "sd", "su", "sl", "sr", "touch", "zr", "zl", "y", "x", "l", "r", "down", "up", "left", "right", "start", "select", "b", "a", "cpaddown", "cpadup", "cpadleft", "cpadright", "spaddown", "spadup", "spadleft", "spadright", "dpaddown", "dpadup", "dpadleft", "dpadright", "dd", "du", "dl", "dr")

	for button in [i.casefold() for i in buttons.split(" ")]:
		for button_code, button_name in zip(button_codes, button_names):
			if button == button_name:
				ret += button_code

	return ret


def resize_image(path, width, height):
	img = Image.open(path)
	img_resized = img.resize((width, height))
	img_resized.save(path)


def save_as_bmp(src_path, dst_path):
	img = Image.open(src_path)
	img.save(dst_path, "bmp")
# End of Functions


# Discord
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents = intents)


@client.event
async def on_ready():
	print(f"We have logged in as {client.user} ({client.user.id})")
	await client.change_presence(activity = discord.Game(name="V.help"))


@client.event
async def on_message(message):
	if message.author == client.user or message.author.bot or (not message.content.casefold().startswith("v.")):
		return

	splitted = message.content[2:].split(" ")
	command = splitted[0].casefold()
	args = splitted[1:]


	# "Help"
	if command == "help":
		await message.reply(help_messages.get(args[0] if len(args) else "ja"))
	# End of "Help"

	if command == "about":
		await message.reply(
"""```
Vermouth BOT by Hidegon

Source code: https://github.com/HidegonSan/VermouthBOT
```"""
		)


	# "Bg"
	if command == "bg":
		if not os.path.exists("./tmp"): os.mkdir("./tmp")

		try:
			for attachment in message.attachments:
				path = "./tmp/" + attachment.filename
				await attachment.save(path)

				# Top
				resize_image(path, 340, 200)
				save_as_bmp(path, os.path.dirname(path) + "/" + "Topbackground.bmp")
				await message.reply("`TOP (340x200)`", file = discord.File(os.path.dirname(path) + "/" + "Topbackground.bmp"))

				# Bottom
				resize_image(path, 280, 200)
				save_as_bmp(path, os.path.dirname(path) + "/" + "Bottombackground.bmp")
				await message.reply("`BOTTOM (280x200)`", file = discord.File(os.path.dirname(path) + "/" + "Bottombackground.bmp"))

			shutil.rmtree("./tmp")
		except Exception as e:
			await message.reply("`エラーが発生しました`")
	# End of "Bg"


	# "SVC"
	if command == "svc":
		try:
			await message.reply(f"`{svc_table.get(args[0], 'SVC Not found.')}`")
		except:
			await message.reply("`エラーが発生しました`")
	# End of "SVC"


	# "Kcd"
	if command == "kcd":
		try:
			await message.reply(f"`{key_to_str(int(' '.join(args), 16))}`")
		except:
			await message.reply("`エラーが発生しました`")
	# End of "Kcd"


	# "Key"
	if command == "key":
		try:
			await message.reply(f"`{hex(button_to_code(' '.join(args)))[2:].upper().zfill(8)}`")
		except Exception as e:
			print(e)
			await message.reply("`エラーが発生しました`")
	# End of "Key"



if os.path.exists("token") and os.path.isfile("token"):
	with open("token", "r") as fr:
		TOKEN = fr.read()
else:
	print("'token' not found.")
	sys.exit(1)

client.run(TOKEN)
